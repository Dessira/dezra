from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def get_shop_token():
    shop_data = {
        "email": "shopx@example.com",
        "password": "shopsecure"
    }
    return client.post("/shop/login", json=shop_data).json()["access_token"]

def test_create_item():
    token = get_shop_token()
    headers = {"Authorization": f"Bearer {token}"}
    item_data = {
        "name": "Test Item",
        "description": "Test description",
        "image": None,
        "expiry_date": "2099-12-31"
    }
    response = client.post("/item/", json=item_data, headers=headers)
    assert response.status_code == 200, response.json()
    item = response.json()
    assert item["name"] == item_data["name"]
    assert "id" in item
    global ITEM_ID
    ITEM_ID = item["id"]

def test_get_all_items():
    response = client.get("/item/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_single_item():
    response = client.get(f"/item/{ITEM_ID}")
    assert response.status_code == 200
    assert response.json()["id"] == ITEM_ID

def test_update_item():
    token = get_shop_token()
    headers = {"Authorization": f"Bearer {token}"}
    update_data = {
        "name": "Updated Item Name",
        "description": "Updated description"
    }
    response = client.put(f"/item/{ITEM_ID}", json=update_data, headers=headers)
    assert response.status_code == 200
    assert response.json()["name"] == update_data["name"]

def test_delete_item():
    token = get_shop_token()
    headers = {"Authorization": f"Bearer {token}"}
    response = client.delete(f"/item/{ITEM_ID}", headers=headers)
    assert response.status_code == 200
    assert response.json()["detail"] == "Item deleted successfully"
