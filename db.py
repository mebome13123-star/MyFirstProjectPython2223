import sqlite3


class Database:
    """Класс для работы с базой данных SQLite."""

    def __init__(self, db_name="shop.db"):
        self.db_name = db_name
        self.connection = sqlite3.connect(self.db_name)
        self.create_tables()

    def create_tables(self):
        """Создаёт таблицы базы данных."""
        cursor = self.connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS clients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                phone TEXT NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                price REAL NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                client_id INTEGER NOT NULL,
                order_date TEXT NOT NULL,
                FOREIGN KEY (client_id) REFERENCES clients(id)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS order_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id INTEGER NOT NULL,
                product_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL,
                FOREIGN KEY (order_id) REFERENCES orders(id),
                FOREIGN KEY (product_id) REFERENCES products(id)
            )
        """)

        self.connection.commit()

    def add_client(self, name, email, phone):
        """Добавляет клиента в базу."""
        cursor = self.connection.cursor()

        cursor.execute(
            """
            INSERT INTO clients (name, email, phone)
            VALUES (?, ?, ?)
            """,
            (name, email, phone)
        )

        self.connection.commit()

    def get_clients(self):
        """Возвращает всех клиентов."""
        cursor = self.connection.cursor()

        cursor.execute(
            "SELECT id, name, email, phone FROM clients"
        )

        return cursor.fetchall()

    def add_product(self, name, price):
        """Добавляет товар в базу."""
        cursor = self.connection.cursor()

        cursor.execute(
            """
            INSERT INTO products (name, price)
            VALUES (?, ?)
            """,
            (name, price)
        )

        self.connection.commit()

    def get_products(self):
        """Возвращает все товары."""
        cursor = self.connection.cursor()

        cursor.execute(
            "SELECT id, name, price FROM products"
        )

        return cursor.fetchall()

    def close(self):
        def add_order(self, client_id, product_id, quantity):
            """Добавляет заказ."""

            cursor = self.connection.cursor()

            cursor.execute(
                """
                INSERT INTO orders (client_id, order_date)
                VALUES (?, datetime('now'))
                """,
                (client_id,)
            )

            order_id = cursor.lastrowid

            cursor.execute(
                """
                INSERT INTO order_items
                (order_id, product_id, quantity)
                VALUES (?, ?, ?)
                """,
                (
                    order_id,
                    product_id,
                    quantity
                )
            )

            self.connection.commit()

    def add_order(self, client_id, product_id, quantity):
        """Добавляет заказ."""

        cursor = self.connection.cursor()

        cursor.execute(
            """
            INSERT INTO orders (client_id, order_date)
            VALUES (?, datetime('now'))
            """,
            (client_id,)
        )

        order_id = cursor.lastrowid

        cursor.execute(
            """
            INSERT INTO order_items
            (order_id, product_id, quantity)
            VALUES (?, ?, ?)
            """,
            (order_id, product_id, quantity)
        )

        self.connection.commit()

    def get_orders(self):
        """Получает список заказов."""

        cursor = self.connection.cursor()

        cursor.execute(
            """
            SELECT
                orders.id,
                clients.name,
                products.name,
                order_items.quantity,
                products.price,
                order_items.quantity * products.price,
                orders.order_date
            FROM orders
            JOIN clients
                ON orders.client_id = clients.id
            JOIN order_items
                ON orders.id = order_items.order_id
            JOIN products
                ON order_items.product_id = products.id
            ORDER BY orders.id DESC
            """
        )

        return cursor.fetchall()

    def close(self):
        """Закрывает соединение с базой."""

        self.connection.close()