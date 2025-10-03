

def test_logging_endpoint(client):
    r = client.get("/api/reports/test_logging")
    assert r.status_code == 200
    data = r.json()
    assert "message" in data


def test_orders_report_empty(client):
    r = client.get("/api/reports/orders")

    assert r.status_code in (200, 404)
