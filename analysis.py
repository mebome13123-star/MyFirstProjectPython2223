from collections import Counter


def top_clients(orders, limit=5):
    clients = []

    for order in orders:
        clients.append(order[1])

    counter = Counter(clients)

    return counter.most_common(limit)


def orders_by_date(orders):
    dates = []

    for order in orders:
        date_value = order[6]

        if date_value:
            date_value = str(date_value)[:10]
            dates.append(date_value)

    counter = Counter(dates)

    return dict(sorted(counter.items()))


def calculate_total(order):
    quantity = order[3]
    price = order[4]

    return quantity * price


def sort_orders_by_price(orders, reverse=True):
    return sorted(
        orders,
        key=calculate_total,
        reverse=reverse
    )