from fastapi.testclient import TestClient
import pytest
import mongomock
from app import app
from application.users import User
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

@pytest.fixture()
def test_app(set_up_mongo: None, set_up_db: None):
    with TestClient(app) as test_client:
        yield test_client
    
def test_create_users(set_up_mongo: None, test_app: TestClient):
    new_user = {
                    "id": "idtest",
                    "name": "jose",
                    "lastname": "pruebas",
                    "email": "pruebas@gmail.com"
                }
    
    response = test_app.post(url='/users', json=new_user)
    assert response.status_code == 200
    assert response.json()["name"] == "jose"

def test_get_all_users(set_up_mongo: None, test_app: TestClient):
    new_user = {
                    "id": "idtest",
                    "name": "jose",
                    "lastname": "pruebas",
                    "email": "pruebas@gmail.com"
                }
    
    test_app.post(url='/users', json=new_user)
    response = test_app.get(url='/users')
    assert response.status_code == 200
    assert response.json() != []

def test_get_one_user(set_up_mongo: None, test_app: TestClient):
    new_user = {
                    "id": "idtest",
                    "name": "jose",
                    "lastname": "pruebas",
                    "email": "pruebas@gmail.com"
                }
    
    response_post = test_app.post(url='/users', json=new_user)
    inserted_id = response_post.json()["id"]
    response = test_app.get(url='/users' + '/' + inserted_id)
    assert response.status_code == 200
    assert response.json()["name"] == "jose"

def test_update_one_user(set_up_mongo: None, test_app: TestClient):
    new_user = {
                    "id": "idtest",
                    "name": "jose",
                    "lastname": "pruebas",
                    "email": "pruebas@gmail.com"
                }
    
    response_post = test_app.post(url='/users', json=new_user)
    inserted_id = response_post.json()["id"]
    updated_user = {
                        "id": "idtest",
                        "name": "nuevo jose",
                        "lastname": "pruebas",
                        "email": "pruebas@gmail.com"
                    }
    response = test_app.put(url='/users' + '/' + inserted_id, json=updated_user)
    assert response.status_code == 200
    assert response.json()["name"] == "nuevo jose"

def test_delete_one_user(set_up_mongo: None, test_app: TestClient):
    new_user = {
                    "id": "idtest",
                    "name": "jose",
                    "lastname": "pruebas",
                    "email": "pruebas@gmail.com"
                }
    
    response_post = test_app.post(url='/users', json=new_user)
    inserted_id = response_post.json()["id"]
    response = test_app.delete(url='/users' + '/' + inserted_id)
    assert response.status_code == 204
