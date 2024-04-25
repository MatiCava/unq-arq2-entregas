from typing import Any
from fastapi.testclient import TestClient
import pytest
import mongomock
from app import app
from domain.products import Product
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
    new_seller = {
                    "id": "idseller",
                    "email": "newsellertest@gmail.com",
                    "razon_social": "1236457"
                }
    response = test_app.post(url='/sellers', json=new_seller)
    return response.json()
    
def test_create_product(set_up_mongo: None, test_app: TestClient, set_up_data: dict):
    seller_id = set_up_data["id"]
    new_prod = {
                    "id": "idprod",
                    "name": "new prod test",
                    "description": "test fresco del horno",
                    "category": "Vehiculos",
                    "price": 10,
                    "stock": 1,
                    "seller_id": seller_id
                }
    response = test_app.post(url='/products', json=new_prod)
    response_seller = test_app.get(url='/sellers' + '/' + seller_id)
    assert response.status_code == 200
    assert response.json()["name"] == "new prod test"
    assert response_seller.json()["list_products"] != []

def test_get_all_products(set_up_mongo: None, test_app: TestClient, set_up_data: dict):
    seller_id = set_up_data["id"]
    new_prod = {
                    "id": "idprod",
                    "name": "new prod test",
                    "description": "test fresco del horno",
                    "category": "Vehiculos",
                    "price": 10,
                    "stock": 1,
                    "seller_id": seller_id
                }
    response = test_app.post(url='/products', json=new_prod)
    response = test_app.get(url='/products')
    assert response.status_code == 200
    assert response.json() != []

def test_get_one_product(set_up_mongo: None, test_app: TestClient, set_up_data: dict):
    seller_id = set_up_data["id"]
    new_prod = {
                    "id": "idprod",
                    "name": "new prod test",
                    "description": "test fresco del horno",
                    "category": "Vehiculos",
                    "price": 10,
                    "stock": 1,
                    "seller_id": seller_id
                }
    response_post = test_app.post(url='/products', json=new_prod)
    inserted_id = response_post.json()["id"]
    response = test_app.get(url='/products' + '/' + inserted_id)
    assert response.status_code == 200
    assert response.json()["name"] == "new prod test"

def test_update_one_product(set_up_mongo: None, test_app: TestClient, set_up_data: dict):
    seller_id = set_up_data["id"]
    new_prod = {
                    "id": "idprod",
                    "name": "new prod test",
                    "description": "test fresco del horno",
                    "category": "Vehiculos",
                    "price": 10,
                    "stock": 1,
                    "seller_id": seller_id
                }
    response_post = test_app.post(url='/products', json=new_prod)
    inserted_id = response_post.json()["id"]
    updated_prod = {
                        "id": "idprod",
                        "name": "new prod updated test",
                        "description": "test fresco del horno",
                        "category": "Vehiculos",
                        "price": 10,
                        "stock": 1,
                        "seller_id": seller_id
                    }
    response = test_app.put(url='/products' + '/' + inserted_id, json=updated_prod)
    assert response.status_code == 200
    assert response.json()["name"] == "new prod updated test"

def test_delete_one_product(set_up_mongo: None, test_app: TestClient, set_up_data: dict):
    seller_id = set_up_data["id"]
    new_prod = {
                    "id": "idprod",
                    "name": "new prod test",
                    "description": "test fresco del horno",
                    "category": "Vehiculos",
                    "price": 10,
                    "stock": 1,
                    "seller_id": seller_id
                }
    response_post = test_app.post(url='/products', json=new_prod)
    inserted_id = response_post.json()["id"]
    response = test_app.delete(url='/products' + '/' + inserted_id)
    assert response.status_code == 204
