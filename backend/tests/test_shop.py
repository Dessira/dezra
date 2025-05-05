from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_register_shop():
    shop_data = {
        "name": "ShopX",
        "email": "shopx@example.com",
        "password": "shopsecure",
        "description": "Test shop",
        "image": None,
        "address": "12 Some Rd",
        "state": "StateX",
        "city": "CityX",
        "country": "CountryX"
    }
    response = client.post("/shop/", json=shop_data)
    assert response.status_code == 200, response.json()
    assert "id" in response.json()
    assert response.json()["name"] == shop_data["name"]

def test_login_shop():
    login_data = {
        "email": "shopx@example.com",
        "password": "shopsecure"
    }
    response = client.post("/shop/login", json=login_data)
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_get_own_shop():
    login_data = {
        "email": "shopx@example.com",
        "password": "shopsecure"
    }
    token = client.post("/shop/login", json=login_data).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/shop/me", headers=headers)
    assert response.status_code == 200
    assert response.json()["email"] == login_data["email"]
