from typing import Any
from fastapi.testclient import TestClient
import pytest
import mongomock
from app import app
from application.sellers import Seller
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
                    "razon_social": "1236457",
                    "list_products": [
                        {
                            "id": "idprod",
                            "name": "new prod test",
                            "description": "test fresco del horno",
                            "category": "Vehiculos",
                            "price": 10,
                            "stock": 2,
                            "seller_id": "randomid"
                        }
                    ]
                }
    response_seller = test_app.post(url='/sellers', json=new_seller)
    inserted_id = response_seller.json()["list_products"][0]["id"]
    response_prod = test_app.get(url='/products' + '/' + inserted_id)
    return response_seller.json(), response_prod.json()

def test_create_seller(set_up_mongo: None, test_app: TestClient, set_up_data: Any):
    info_seller, info_prod = set_up_data
    new_seller = {
                    "id": "idseller",
                    "email": "newsellertest2@gmail.com",
                    "razon_social": "44444",
                    "list_products": [
                        {
                            "id": "idprod",
                            "name": "new prod test 2",
                            "description": "test fresco del horno 2",
                            "category": "Vehiculos",
                            "price": 100,
                            "stock": 1,
                            "seller_id": "randomid"
                        }
                    ]
                }
    response_seller = test_app.post(url='/sellers', json=new_seller)
    assert response_seller.status_code == 200
    assert response_seller.json()["razon_social"] == "44444"
    assert response_seller.json()["list_products"] != []

def test_get_one_seller(set_up_mongo: None, test_app: TestClient, set_up_data: Any):
    info_seller, info_prod = set_up_data
    inserted_id = info_seller["id"]
    response = test_app.get(url='/sellers' + '/' + inserted_id)
    assert response.status_code == 200
    assert response.json()["razon_social"] == "1236457"
    assert response.json()["list_products"] != []

def test_update_one_seller(set_up_mongo: None, test_app: TestClient, set_up_data: Any):
    info_seller, info_prod = set_up_data
    inserted_id = info_seller["id"]
    updated_seller = {
                        "id": "idseller",
                        "email": "updatedmail@gmail.com",
                        "razon_social": "22222"
                    }
    response = test_app.put(url='/sellers' + '/' + inserted_id, json=updated_seller)
    assert response.status_code == 200
    assert response.json()["razon_social"] == "22222"
    assert response.json()["email"] == "updatedmail@gmail.com"
    assert response.json()["list_products"] != []

def test_get_all_seller(set_up_mongo: None, test_app: TestClient, set_up_data: Any):
    info_seller, info_prod = set_up_data
    response = test_app.get(url='/sellers')
    assert response.status_code == 200
    assert response.json() != []

def test_delete_one_seller(set_up_mongo: None, test_app: TestClient, set_up_data: Any):
    info_seller, info_prod = set_up_data
    inserted_id = info_seller["id"]
    response = test_app.delete(url='/sellers' + '/' + inserted_id)
    response_prod = test_app.get(url='/products' + '/' + info_prod["id"])
    assert response.status_code == 204
    assert response_prod.status_code == 400