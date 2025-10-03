
import pytest
from conftest import create_user, login_and_get_token

def test_create_get_update_delete_product(client, db_session):

    admin = create_user(db_session, "admin@test.com", "admin123", is_admin=True)
    token = login_and_get_token(client, "admin@test.com", "admin123")


    r = client.post("/api/products/", json={
        "name": "Test Product",
        "sku": "TP001",
        "price": 10.0,
        "qty_in_stock": 5
    }, headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200
    product_id = r.json()["id"]


    r2 = client.get(f"/api/products/{product_id}", headers={"Authorization": f"Bearer {token}"})
    assert r2.status_code == 200


    r3 = client.put(f"/api/products/{product_id}", json={
        "name": "Updated Product",
        "sku": "TP001",
        "price": 12.0,
        "qty_in_stock": 10
    }, headers={"Authorization": f"Bearer {token}"})
    assert r3.status_code == 200
    assert r3.json()["name"] == "Updated Product"


    r4 = client.delete(f"/api/products/{product_id}", headers={"Authorization": f"Bearer {token}"})
    assert r4.status_code == 200
