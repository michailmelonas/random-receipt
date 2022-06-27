from random_receipt.app import app


def test_random_receipt_endpoint():
    client = app.test_client()
    response = client.get('/api/receipt')

    assert response.status_code == 200
    assert isinstance(response.json, dict)
