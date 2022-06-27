import csv
import pathlib
import random

import names


_MIN_ITEMS = 5
_MAX_ITEMS = 20
_MAX_PRICE = 100000
_MAX_QUANTITY = 5
_VAT_PERCENTAGE = 15

_PRODUCTS = []
with open(pathlib.Path(__file__).parent.joinpath("data/groceries.csv"), "r") as f:
    reader = csv.reader(f)
    for row in reader:
        _PRODUCTS.append(row[1].title())


def generate():
    item_count = random.randint(_MIN_ITEMS, _MAX_ITEMS)
    items = random.sample(_PRODUCTS, item_count)

    line_items = []
    total = 0
    for item in items:
        price = random.randint(1, _MAX_PRICE)
        quantity = random.randint(1, _MAX_QUANTITY)
        item_total = price * quantity

        line_items.append({
            "description": item,
            "price": price,
            "quantity": quantity,
            "total": item_total
        })
        total += item_total

    return {
        "lineItems": line_items,
        "total": total,
        "tax": round(_VAT_PERCENTAGE / (100 + _VAT_PERCENTAGE) * total),
        "storeName": names.get_last_name() + "'s Store",
        "logoUrl": "https://picsum.photos/200/100"
    }
