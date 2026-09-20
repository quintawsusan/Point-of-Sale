import os
import pytest 
from fastapi.testclient import TestClient
import fastapi.testclient as fastapi_testclient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

os.environ["DATABASE_URL"] = "sqlite://"

from app.database import Base, get_db
from app.main import app

engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)

TestingSessionLocal = sessionmaker(bind=engine)

@pytest.fixture
def client():
    Base.metadata.create_all(bind=engine)
    
    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()
            
    app.dependency_overrides[get_db] = override_get_db
    
    yield TestClient(app)
    
    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)
    
# @pytest.fixture
# def test_user(client):
#     user_data = {
#         "username": "testuser",
#         "password": "testpassword",
#         "email": "hRb4B@example.com",
#     }
    
#     client.post("/auth/register", json=user_data)
#     return user_data

# @pytest.fixture
# def auth_headers(client, test_user):
#     response = client.post(
#         "/auth/login",
#         data={"username": test_user["username"], "password": test_user["password"]},
#     )
#     token = response.json()["access_token"]
#     return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def test_user(client):
    user_data = {
        "username": "testuser",
        "password": "testpassword",
        "role": "cashier",
    }

    response = client.post("/auth/register", json=user_data)

    assert response.status_code == 201, (
        f"Registration failed: {response.status_code} - {response.text}"
    )

    return user_data

@pytest.fixture
def auth_headers(client, test_user):
    response = client.post(
        "/auth/login",
        data={
            "username": test_user["username"],
            "password": test_user["password"],
        },
    )

    assert response.status_code == 200, (f"Login failed: {response.status_code} - {response.text}")
    data = response.json()
    assert "access_token" in data, (f"Login response does not contain access_token: {data}")
    return {"Authorization": f"Bearer {data['access_token']}"}   
    
