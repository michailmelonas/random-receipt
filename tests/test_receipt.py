import random

from random_receipt.receipt import generate


def test_receipt_contains_required_fields():
    receipt = generate()
    required_fields = ["total", "lineItems", "tax", "storeName", "logoUrl"]
    assert all([k in required_fields for k in receipt.keys()])


def test_item_totals_match_grand_total():
    receipt = generate()
    assert sum([item["total"] for item in receipt["lineItems"]]) == receipt["total"]
