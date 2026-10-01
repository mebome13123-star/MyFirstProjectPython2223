import re
from datetime import datetime


class Person:
    """Базовый класс человека."""

    def __init__(self, name):
        self.name = name

    def get_info(self):
        """Возвращает информацию о человеке."""
        return f"Имя: {self.name}"


class Client(Person):
    """Класс клиента интернет-магазина."""

    def __init__(self, name, email, phone):
        super().__init__(name)
        self._email = None
        self._phone = None

        self.email = email
        self.phone = phone

    @property
    def email(self):
        """Возвращает email клиента."""
        return self._email

    @email.setter
    def email(self, value):
        """Устанавливает email после проверки."""
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"

        if not re.match(pattern, value):
            raise ValueError("Некорректный email")

        self._email = value

    @property
    def phone(self):
        """Возвращает телефон клиента."""
        return self._phone

    @phone.setter
    def phone(self, value):
        """Устанавливает телефон после проверки."""
        pattern = r"^\+?[0-9\s\-\(\)]{10,20}$"

        if not re.match(pattern, value):
            raise ValueError("Некорректный номер телефона")

        self._phone = value

    def get_info(self):
        """Возвращает информацию о клиенте."""
        return f"{self.name} | {self.email} | {self.phone}"


class Product:
    """Класс товара."""

    def __init__(self, name, price):
        if price < 0:
            raise ValueError("Цена не может быть отрицательной")

        self.name = name
        self.price = price

    def get_info(self):
        """Возвращает информацию о товаре."""
        return f"{self.name} — {self.price:.2f} руб."


class Order:
    """Класс заказа."""

    def __init__(self, client, date=None):
        self.client = client
        self.date = date or datetime.now()
        self.products = []

    def add_product(self, product, quantity=1):
        """Добавляет товар в заказ."""
        if quantity <= 0:
            raise ValueError("Количество должно быть больше нуля")

        self.products.append((product, quantity))

    def get_total(self):
        """Возвращает общую стоимость заказа."""
        return sum(product.price * quantity
                   for product, quantity in self.products)

    def get_info(self):
        """Возвращает информацию о заказе."""
        return (
            f"Заказ клиента: {self.client.name}, "
            f"товаров: {len(self.products)}, "
            f"сумма: {self.get_total():.2f} руб."
        )


class VIPClient(Client):
    """Клиент с VIP-статусом."""

    def get_info(self):
        """Возвращает расширенную информацию о VIP-клиенте."""
        return f"[VIP] {super().get_info()}"