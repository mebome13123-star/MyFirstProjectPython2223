import tkinter as tk
from tkinter import ttk, messagebox

from db import Database
from analysis import top_clients, orders_by_date, sort_orders_by_price
from export_import import (
    export_to_csv,
    import_from_csv,
    export_to_json,
    import_from_json
)

class ShopApp:
    """Графическое приложение для учёта интернет-магазина."""

    def __init__(self, root):
        self.root = root
        self.root.title("Система учёта интернет-магазина")
        self.root.geometry("1000x700")

        self.db = Database()

        self.clients_data = []
        self.products_data = []

        self.create_interface()

        self.load_clients()
        self.load_products()
        self.load_order_options()
        self.load_orders()
        self.update_analysis()

    def create_interface(self):
        """Создаёт интерфейс приложения."""

        title = tk.Label(
            self.root,
            text="Система учёта интернет-магазина",
            font=("Arial", 20, "bold")
        )

        title.pack(pady=15)

        notebook = ttk.Notebook(self.root)
        notebook.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=10
        )

        self.clients_tab = ttk.Frame(notebook)
        self.products_tab = ttk.Frame(notebook)
        self.orders_tab = ttk.Frame(notebook)
        self.analysis_tab = ttk.Frame(notebook)

        notebook.add(
            self.clients_tab,
            text="Клиенты"
        )

        notebook.add(
            self.products_tab,
            text="Товары"
        )

        notebook.add(
            self.orders_tab,
            text="Заказы"
        )

        notebook.add(
            self.analysis_tab,
            text="Анализ"
        )

        self.create_clients_tab()
        self.create_products_tab()
        self.create_orders_tab()
        self.create_analysis_tab()

    # =========================================================
    # КЛИЕНТЫ
    # =========================================================

    def create_clients_tab(self):
        form = ttk.LabelFrame(
            self.clients_tab,
            text="Добавление клиента"
        )

        form.pack(
            fill="x",
            padx=10,
            pady=10
        )

        ttk.Label(
            form,
            text="Имя:"
        ).grid(
            row=0,
            column=0,
            padx=5,
            pady=8
        )

        self.client_name = ttk.Entry(
            form,
            width=35
        )

        self.client_name.grid(
            row=0,
            column=1,
            padx=5,
            pady=8
        )

        ttk.Label(
            form,
            text="Email:"
        ).grid(
            row=1,
            column=0,
            padx=5,
            pady=8
        )

        self.client_email = ttk.Entry(
            form,
            width=35
        )

        self.client_email.grid(
            row=1,
            column=1,
            padx=5,
            pady=8
        )

        ttk.Label(
            form,
            text="Телефон:"
        ).grid(
            row=2,
            column=0,
            padx=5,
            pady=8
        )

        self.client_phone = ttk.Entry(
            form,
            width=35
        )

        self.client_phone.grid(
            row=2,
            column=1,
            padx=5,
            pady=8
        )

        ttk.Button(
            form,
            text="Добавить клиента",
            command=self.add_client
        ).grid(
            row=3,
            column=0,
            columnspan=2,
            pady=10
        )

        search_frame = ttk.Frame(
            self.clients_tab
        )

        search_frame.pack(
            fill="x",
            padx=10,
            pady=5
        )

        ttk.Label(
            search_frame,
            text="Поиск:"
        ).pack(
            side="left",
            padx=5
        )

        self.client_search = ttk.Entry(
            search_frame,
            width=30
        )

        self.client_search.pack(
            side="left",
            padx=5
        )

        ttk.Button(
            search_frame,
            text="Найти",
            command=self.search_clients
        ).pack(
            side="left",
            padx=5
        )

        ttk.Button(
            search_frame,
            text="Показать всех",
            command=self.load_clients
        ).pack(
            side="left",
            padx=5
        )

        table_frame = ttk.Frame(
            self.clients_tab
        )

        table_frame.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        self.clients_table = ttk.Treeview(
            table_frame,
            columns=(
                "id",
                "name",
                "email",
                "phone"
            ),
            show="headings"
        )

        self.clients_table.heading(
            "id",
            text="ID"
        )

        self.clients_table.heading(
            "name",
            text="Имя"
        )

        self.clients_table.heading(
            "email",
            text="Email"
        )

        self.clients_table.heading(
            "phone",
            text="Телефон"
        )

        self.clients_table.pack(
            fill="both",
            expand=True
        )

    def add_client(self):
        """Добавляет клиента."""

        name = self.client_name.get().strip()
        email = self.client_email.get().strip()
        phone = self.client_phone.get().strip()

        if not name or not email or not phone:
            messagebox.showwarning(
                "Ошибка",
                "Заполните все поля."
            )
            return

        try:
            self.db.add_client(
                name,
                email,
                phone
            )

            messagebox.showinfo(
                "Успех",
                "Клиент успешно добавлен!"
            )

            self.client_name.delete(0, tk.END)
            self.client_email.delete(0, tk.END)
            self.client_phone.delete(0, tk.END)

            self.load_clients()
            self.load_order_options()
            self.update_analysis()

        except Exception as error:
            messagebox.showerror(
                "Ошибка",
                str(error)
            )

    def load_clients(self):
        if not hasattr(self, "clients_table"):
            return

        for item in self.clients_table.get_children():
            self.clients_table.delete(item)

        clients = self.db.get_clients()

        for client in clients:
            self.clients_table.insert(
                "",
                "end",
                values=client
            )

    def search_clients(self):
        search_text = (
            self.client_search
            .get()
            .strip()
            .lower()
        )

        for item in self.clients_table.get_children():
            self.clients_table.delete(item)

        clients = self.db.get_clients()

        for client in clients:
            name = str(client[1]).lower()
            email = str(client[2]).lower()

            if (
                search_text in name
                or search_text in email
            ):
                self.clients_table.insert(
                    "",
                    "end",
                    values=client
                )

    # =========================================================
    # ТОВАРЫ
    # =========================================================

    def create_products_tab(self):
        form = ttk.LabelFrame(
            self.products_tab,
            text="Добавление товара"
        )

        form.pack(
            fill="x",
            padx=10,
            pady=10
        )

        ttk.Label(
            form,
            text="Название:"
        ).grid(
            row=0,
            column=0,
            padx=5,
            pady=8
        )

        self.product_name = ttk.Entry(
            form,
            width=35
        )

        self.product_name.grid(
            row=0,
            column=1,
            padx=5,
            pady=8
        )

        ttk.Label(
            form,
            text="Цена:"
        ).grid(
            row=1,
            column=0,
            padx=5,
            pady=8
        )

        self.product_price = ttk.Entry(
            form,
            width=35
        )

        self.product_price.grid(
            row=1,
            column=1,
            padx=5,
            pady=8
        )

        ttk.Button(
            form,
            text="Добавить товар",
            command=self.add_product
        ).grid(
            row=2,
            column=0,
            columnspan=2,
            pady=10
        )

        self.products_table = ttk.Treeview(
            self.products_tab,
            columns=(
                "id",
                "name",
                "price"
            ),
            show="headings"
        )

        self.products_table.heading(
            "id",
            text="ID"
        )

        self.products_table.heading(
            "name",
            text="Название"
        )

        self.products_table.heading(
            "price",
            text="Цена"
        )

        self.products_table.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

    def add_product(self):
        name = self.product_name.get().strip()
        price_text = self.product_price.get().strip()

        if not name or not price_text:
            messagebox.showwarning(
                "Ошибка",
                "Заполните все поля."
            )
            return

        try:
            price = float(price_text)

            if price < 0:
                raise ValueError(
                    "Цена не может быть отрицательной."
                )

            self.db.add_product(
                name,
                price
            )

            messagebox.showinfo(
                "Успех",
                "Товар успешно добавлен!"
            )

            self.product_name.delete(0, tk.END)
            self.product_price.delete(0, tk.END)

            self.load_products()
            self.load_order_options()

        except ValueError as error:
            messagebox.showerror(
                "Ошибка",
                str(error)
            )

        except Exception as error:
            messagebox.showerror(
                "Ошибка",
                str(error)
            )

    def load_products(self):
        if not hasattr(self, "products_table"):
            return

        for item in self.products_table.get_children():
            self.products_table.delete(item)

        products = self.db.get_products()

        for product in products:
            self.products_table.insert(
                "",
                "end",
                values=product
            )

    # =========================================================
    # ЗАКАЗЫ
    # =========================================================

    def create_orders_tab(self):
        form = ttk.LabelFrame(
            self.orders_tab,
            text="Создание заказа"
        )

        form.pack(
            fill="x",
            padx=10,
            pady=10
        )

        ttk.Label(
            form,
            text="Клиент:"
        ).grid(
            row=0,
            column=0,
            padx=5,
            pady=8
        )

        self.order_client = ttk.Combobox(
            form,
            width=35,
            state="readonly"
        )

        self.order_client.grid(
            row=0,
            column=1,
            padx=5,
            pady=8
        )

        ttk.Label(
            form,
            text="Товар:"
        ).grid(
            row=1,
            column=0,
            padx=5,
            pady=8
        )

        self.order_product = ttk.Combobox(
            form,
            width=35,
            state="readonly"
        )

        self.order_product.grid(
            row=1,
            column=1,
            padx=5,
            pady=8
        )

        ttk.Label(
            form,
            text="Количество:"
        ).grid(
            row=2,
            column=0,
            padx=5,
            pady=8
        )

        self.order_quantity = ttk.Entry(
            form,
            width=38
        )

        self.order_quantity.insert(
            0,
            "1"
        )

        self.order_quantity.grid(
            row=2,
            column=1,
            padx=5,
            pady=8
        )

        ttk.Button(
            form,
            text="Создать заказ",
            command=self.add_order
        ).grid(
            row=3,
            column=0,
            columnspan=2,
            pady=10
        )
        # Кнопки импорта и экспорта
        export_frame = ttk.Frame(self.orders_tab)
        export_frame.pack(fill="x", padx=10, pady=5)

        ttk.Button(
            export_frame,
            text="Экспорт CSV",
            command=self.export_csv
        ).pack(side="left", padx=5)

        ttk.Button(
            export_frame,
            text="Импорт CSV",
            command=self.import_csv
        ).pack(side="left", padx=5)

        ttk.Button(
            export_frame,
            text="Экспорт JSON",
            command=self.export_json
        ).pack(side="left", padx=5)

        ttk.Button(
            export_frame,
            text="Импорт JSON",
            command=self.import_json
        ).pack(side="left", padx=5)

        self.orders_table = ttk.Treeview(
            self.orders_tab,
            columns=(
                "id",
                "client",
                "product",
                "quantity",
                "price",
                "total",
                "date"
            ),
            show="headings"
        )

        headings = {
            "id": "ID",
            "client": "Клиент",
            "product": "Товар",
            "quantity": "Количество",
            "price": "Цена",
            "total": "Сумма",
            "date": "Дата"
        }

        for column, heading in headings.items():
            self.orders_table.heading(
                column,
                text=heading
            )

        self.orders_table.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

    def load_order_options(self):
        if not hasattr(self, "order_client"):
            return

        self.clients_data = self.db.get_clients()
        self.products_data = self.db.get_products()

        self.order_client["values"] = [
            f"{client[0]} — {client[1]}"
            for client in self.clients_data
        ]

        self.order_product["values"] = [
            f"{product[0]} — {product[1]}"
            for product in self.products_data
        ]

    def add_order(self):
        client_index = self.order_client.current()
        product_index = self.order_product.current()

        quantity_text = (
            self.order_quantity
            .get()
            .strip()
        )

        if client_index == -1:
            messagebox.showwarning(
                "Ошибка",
                "Выберите клиента."
            )
            return

        if product_index == -1:
            messagebox.showwarning(
                "Ошибка",
                "Выберите товар."
            )
            return

        try:
            quantity = int(quantity_text)

            if quantity <= 0:
                raise ValueError

            client_id = self.clients_data[
                client_index
            ][0]

            product_id = self.products_data[
                product_index
            ][0]

            self.db.add_order(
                client_id,
                product_id,
                quantity
            )

            messagebox.showinfo(
                "Успех",
                "Заказ успешно создан!"
            )

            self.order_quantity.delete(
                0,
                tk.END
            )

            self.order_quantity.insert(
                0,
                "1"
            )

            self.load_orders()
            self.update_analysis()

        except ValueError:
            messagebox.showerror(
                "Ошибка",
                "Количество должно быть положительным целым числом."
            )

        except Exception as error:
            messagebox.showerror(
                "Ошибка",
                str(error)
            )

    def load_orders(self):
        if not hasattr(self, "orders_table"):
            return

        for item in self.orders_table.get_children():
            self.orders_table.delete(item)

        orders = self.db.get_orders()

        for order in orders:
            self.orders_table.insert(
                "",
                "end",
                values=order
            )
    def export_csv(self):
        """Экспортирует заказы в CSV."""

        try:
            orders = self.db.get_orders()
            export_to_csv(orders)

            messagebox.showinfo(
                "Успех",
                "Заказы экспортированы в orders.csv"
            )

        except Exception as error:
            messagebox.showerror(
                "Ошибка",
                str(error)
            )

    def import_csv(self):
        """Импортирует данные из CSV."""

        try:
            data = import_from_csv()

            messagebox.showinfo(
                "Импорт CSV",
                f"Из файла загружено записей: {len(data)}"
            )

        except Exception as error:
            messagebox.showerror(
                "Ошибка",
                str(error)
            )

    def export_json(self):
        """Экспортирует заказы в JSON."""

        try:
            orders = self.db.get_orders()
            export_to_json(orders)

            messagebox.showinfo(
                "Успех",
                "Заказы экспортированы в orders.json"
            )

        except Exception as error:
            messagebox.showerror(
                "Ошибка",
                str(error)
            )

    def import_json(self):
        """Импортирует данные из JSON."""

        try:
            data = import_from_json()

            messagebox.showinfo(
                "Импорт JSON",
                f"Из файла загружено записей: {len(data)}"
            )

        except Exception as error:
            messagebox.showerror(
                "Ошибка",
                str(error)
            )
    # =========================================================
    # АНАЛИЗ
    # =========================================================

    def create_analysis_tab(self):
        """Создаёт вкладку анализа."""

        title = ttk.Label(
            self.analysis_tab,
            text="Анализ данных магазина",
            font=("Arial", 16, "bold")
        )

        title.pack(pady=15)

        self.analysis_info = tk.Label(
            self.analysis_tab,
            text="",
            font=("Arial", 12),
            justify="left"
        )

        self.analysis_info.pack(
            anchor="w",
            padx=30,
            pady=10
        )

        ttk.Button(
            self.analysis_tab,
            text="Обновить анализ",
            command=self.update_analysis
        ).pack(
            pady=10
        )

        clients_frame = ttk.LabelFrame(
            self.analysis_tab,
            text="Топ клиентов"
        )

        clients_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        self.top_clients_table = ttk.Treeview(
            clients_frame,
            columns=(
                "client",
                "orders"
            ),
            show="headings",
            height=5
        )

        self.top_clients_table.heading(
            "client",
            text="Клиент"
        )

        self.top_clients_table.heading(
            "orders",
            text="Количество заказов"
        )

        self.top_clients_table.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        dates_frame = ttk.LabelFrame(
            self.analysis_tab,
            text="Динамика заказов по датам"
        )

        dates_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        self.orders_dates_table = ttk.Treeview(
            dates_frame,
            columns=(
                "date",
                "orders"
            ),
            show="headings",
            height=5
        )

        self.orders_dates_table.heading(
            "date",
            text="Дата"
        )

        self.orders_dates_table.heading(
            "orders",
            text="Количество заказов"
        )

        self.orders_dates_table.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

    def update_analysis(self):
        """Обновляет статистику."""

        if not hasattr(
            self,
            "analysis_info"
        ):
            return

        orders = self.db.get_orders()

        total_orders = len(orders)

        total_sum = 0

        for order in orders:
            total_sum += float(order[5])

        average = 0

        if total_orders > 0:
            average = total_sum / total_orders

        self.analysis_info.config(
            text=(
                f"Всего заказов: {total_orders}\n"
                f"Общая сумма заказов: {total_sum:.2f} руб.\n"
                f"Средняя стоимость заказа: {average:.2f} руб."
            )
        )

        # Топ клиентов

        if hasattr(
            self,
            "top_clients_table"
        ):
            for item in self.top_clients_table.get_children():
                self.top_clients_table.delete(item)

            clients = top_clients(
                orders,
                limit=5
            )

            for client, count in clients:
                self.top_clients_table.insert(
                    "",
                    "end",
                    values=(
                        client,
                        count
                    )
                )

        # Динамика по датам

        if hasattr(
            self,
            "orders_dates_table"
        ):
            for item in self.orders_dates_table.get_children():
                self.orders_dates_table.delete(item)

            dates = orders_by_date(orders)

            for date, count in dates.items():
                self.orders_dates_table.insert(
                    "",
                    "end",
                    values=(
                        date,
                        count
                    )
                )

    # =========================================================
    # ЗАКРЫТИЕ
    # =========================================================

    def close(self):
        """Закрывает приложение."""

        self.db.close()
        self.root.destroy()


def run_app():
    """Запускает приложение."""

    root = tk.Tk()

    app = ShopApp(root)

    root.protocol(
        "WM_DELETE_WINDOW",
        app.close
    )

    root.mainloop()