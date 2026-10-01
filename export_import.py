import csv
import json


def export_to_csv(orders, filename="orders.csv"):
    """Экспортирует список заказов в CSV-файл."""

    headers = [
        "id",
        "client",
        "product",
        "quantity",
        "price",
        "total",
        "order_date"
    ]

    with open(filename, "w", newline="", encoding="utf-8-sig") as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(orders)


def import_from_csv(filename="orders.csv"):
    """Импортирует заказы из CSV-файла."""

    with open(filename, "r", newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        return list(reader)


def export_to_json(orders, filename="orders.json"):
    """Экспортирует список заказов в JSON-файл."""

    headers = [
        "id",
        "client",
        "product",
        "quantity",
        "price",
        "total",
        "order_date"
    ]

    data = []

    for order in orders:
        data.append(dict(zip(headers, order)))

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def import_from_json(filename="orders.json"):
    """Импортирует заказы из JSON-файла."""

    with open(filename, "r", encoding="utf-8") as file:
        return json.load(file)