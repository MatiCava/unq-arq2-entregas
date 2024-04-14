from typing import Any
from fastapi.testclient import TestClient
import pytest
import mongomock
from app import app
from application.sales import Sale
import config.db

@pytest.fixture(autouse=True, scope='module')
def monkeymodule():
    with pytest.MonkeyPatch.context() as mp:
        yield mp

@pytest.fixture(scope="module")
def set_up_mongo(monkeymodule: pytest.MonkeyPatch):
    def fake_client():
        return mongomock.MongoClient()
    monkeymodule.setattr(config.db, 'client', fake_client)

@pytest.fixture(scope="module")
def set_up_db(monkeymodule: pytest.MonkeyPatch):
    def fake_db(fake_client):
        return fake_client.db
    monkeymodule.setattr(config.db, 'db', fake_db)

@pytest.fixture(scope="module")
def test_app(set_up_mongo: None, set_up_db: None):
    with TestClient(app) as test_client:
        yield test_client

@pytest.fixture(scope="module")
def set_up_data(test_app: TestClient):
    new_user = {
                    "id": "idtest",
                    "name": "jose",
                    "lastname": "pruebas",
                    "email": "pruebas@gmail.com"
                }
    
    response_user = test_app.post(url='/users', json=new_user)
    new_seller = {
                    "id": "idseller",
                    "email": "newsellertest@gmail.com",
                    "razon_social": "1236457"
                }
    response_seller = test_app.post(url='/sellers', json=new_seller)
    new_prod = {
                    "id": "idprod",
                    "name": "new prod test",
                    "description": "test fresco del horno",
                    "category": "Vehiculos",
                    "price": 10,
                    "stock": 2,
                    "seller_id": response_seller.json()["id"]
                }
    response_prod = test_app.post(url='/products', json=new_prod)
    new_sale = {
                    "id": "id sale",
                    "date": "2024-04-14",
                    "status": "created",
                    "user_id": response_user.json()["id"],
                    "products_info": [{
                        "product_id": response_prod.json()["id"],
                        "quantity": 1
                    }]
                }
    response_sale = test_app.post(url='/sales', json=new_sale)
    return response_user.json(), response_prod.json(), response_sale.json()

def test_create_sale(set_up_mongo: None, test_app: TestClient, set_up_data: Any):
    info_user, info_prod, info_sale = set_up_data
    new_sale = {
                    "id": "id sale",
                    "date": "2024-04-14",
                    "status": "created",
                    "user_id": info_user["id"],
                    "products_info": [{
                        "product_id": info_prod["id"],
                        "quantity": 1
                    }]
                }
    response = test_app.post(url='/sales', json=new_sale)
    response_post = test_app.get(url='/products' + '/' + info_prod["id"])
    assert response.status_code == 200
    assert response.json()["status"] == "created"
    assert response.json()["user_id"] == info_user["id"]
    assert response.json()["products_info"] != []
    assert response_post.json()["stock"] == 0

def test_get_one_sale(set_up_mongo: None, test_app: TestClient, set_up_data: Any):
    info_user, info_prod, info_sale = set_up_data
    inserted_id = info_sale["id"]
    response = test_app.get(url='/sales' + '/' + inserted_id)
    assert response.status_code == 200
    assert response.json()["status"] == "created"
    assert response.json()["user_id"] == info_user["id"]
    assert response.json()["products_info"] != []

def test_update_one_sale(set_up_mongo: None, test_app: TestClient, set_up_data: Any):
    info_user, info_prod, info_sale = set_up_data
    inserted_id = info_sale["id"]
    updated_sale = {
                        "id": "id sale",
                        "date": "2024-04-14",
                        "status": "created",
                        "user_id": info_user["id"],
                        "products_info": []
                    }
    response = test_app.put(url='/sales' + '/' + inserted_id, json=updated_sale)
    response_prod = test_app.get(url='/products' + '/' + info_prod["id"])
    assert response.status_code == 200
    assert response.status_code == 200
    assert response.json()["status"] == "created"
    assert response.json()["user_id"] == info_user["id"]
    assert response.json()["products_info"] == []
    assert response_prod.json()["stock"] == 1

def test_get_all_sales(set_up_mongo: None, test_app: TestClient, set_up_data: Any):
    info_user, info_prod, info_sale = set_up_data
    response = test_app.get(url='/sales')
    assert response.status_code == 200
    assert response.json() != []

def test_delete_one_sale(set_up_mongo: None, test_app: TestClient, set_up_data: Any):
    info_user, info_prod, info_sale = set_up_data
    inserted_id = info_sale["id"]
    response = test_app.delete(url='/sales' + '/' + inserted_id)
    assert response.status_code == 204