
import pytest
from conftest import create_user, login_and_get_token
from models import Product, Customer

def test_create_get_delete_order(client, db_session):
    admin = create_user(db_session, "admin3@test.com", "admin123", is_admin=True)
    token = login_and_get_token(client, "admin3@test.com", "admin123")


    product = Product(name="Prod1", sku="SKU1", price=10.0, qty_in_stock=10)
    db_session.add(product)
    db_session.commit()
    db_session.refresh(product)


    customer = Customer(full_name="Cust1", email="cust1@test.com", phone="111")
    db_session.add(customer)
    db_session.commit()
    db_session.refresh(customer)


    r = client.post("/api/orders/", json={
        "customer_id": customer.id,
        "items": [{"product_id": product.id, "qty": 2}]
    }, headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200
    order_id = r.json()["id"]


    r2 = client.get(f"/api/orders/{order_id}", headers={"Authorization": f"Bearer {token}"})
    assert r2.status_code == 200


    r3 = client.delete(f"/api/orders/{order_id}", headers={"Authorization": f"Bearer {token}"})
    assert r3.status_code == 200
