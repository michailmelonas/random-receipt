from datetime import datetime
from pathlib import Path
import csv
import random


_MIN_ITEMS = 2
_MAX_ITEMS = 10
_MAX_PRICE = 30000
_MAX_QUANTITY = 3
_VAT_PERCENTAGE = 15

_PRODUCTS = []
with open(Path(__file__).parent.joinpath("data/groceries.csv"), "r") as f:
    reader = csv.reader(f)
    for row in reader:
        _PRODUCTS.append(row[0].title())

_STORES = []
with open(Path(__file__).parent.joinpath("data/stores.csv"), "r") as f:
    reader = csv.reader(f)
    for row in reader:
        _STORES.append({"storeName": row[0], "logoUrl": row[1]})

_GROCERY_LOGOS = []
with open(Path(__file__).parent.joinpath("data/grocery_logos.csv"), "r") as f:
    reader = csv.reader(f)
    for row in reader:
        _GROCERY_LOGOS.append(row[0])


def _convert_cents_to_currency(n: int) -> str:
    return "{0:.2f}".format(n/100)


def generate() -> dict:
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
            "price": _convert_cents_to_currency(price),
            "quantity": quantity,
            "logo": random.sample(_GROCERY_LOGOS, 1)[0],
            "total": _convert_cents_to_currency(item_total)
        })
        total += item_total

    return {
        "lineItems": line_items,
        "total": _convert_cents_to_currency(total),
        "tax": _convert_cents_to_currency(round(_VAT_PERCENTAGE / (100 + _VAT_PERCENTAGE) * total)),
        "datestamp": datetime.now().strftime("%d-%m-%y %H:%M"),
        **random.sample(_STORES, 1)[0]
    }
