from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_register_user():
    user_data = {
        "email": "user1@example.com",
        "first_name": "User",
        "last_name": "One",
        "password": "securepassword"
    }
    response = client.post("/user/", json=user_data)
    assert response.status_code == 200, response.json()
    data = response.json()
    assert data["email"] == user_data["email"]
    assert "id" in data

def test_login_user():
    login_data = {
        "email": "user1@example.com",
        "password": "securepassword"
    }
    response = client.post("/login", json=login_data)
    assert response.status_code == 200, response.json()
    assert "access_token" in response.json()

def test_get_own_user():
    login_data = {
        "email": "user1@example.com",
        "password": "securepassword"
    }
    token = client.post("/login", json=login_data).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/user/me", headers=headers)
    assert response.status_code == 200
    assert response.json()["email"] == login_data["email"]
