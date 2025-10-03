
import pytest

def test_register_login(client, db_session):

    r = client.post("/api/auth/register", json={
        "full_name": "Normal User",
        "email": "user@test.com",
        "password": "test123",
        "is_admin": False
    })
    assert r.status_code in (200, 201)
    data = r.json()
    assert data["email"] == "user@test.com"
    assert not data["is_admin"]


    r2 = client.post("/api/auth/login", json={"email": "user@test.com", "password": "test123"})
    assert r2.status_code == 200
    token = r2.json()["access_token"]
    assert token
