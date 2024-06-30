from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest
from main import app, get_db
from database import Base

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(scope="module")
def test_client():
    return client

def test_create_payment(test_client):
    response = test_client.post(
        "/payments/",
        json={
            "card_number": "1234567812345678",
            "expiry_month": 12,
            "expiry_year": 2024,
            "amount": 100.0,
            "currency": "USD",
            "cvv": 123
        }
    )
    assert response.status_code == 200
    assert response.json()["status"] in ["success", "failure"]

def test_get_payment(test_client):
    create_response = test_client.post(
        "/payments/",
        json={
            "card_number": "1234567812345678",
            "expiry_month": 12,
            "expiry_year": 2024,
            "amount": 100.0,
            "currency": "USD",
            "cvv": 123
        }
    )
    payment_id = create_response.json()["id"]
    get_response = test_client.get(f"/payments/{payment_id}")
    assert get_response.status_code == 200
    assert get_response.json()["id"] == payment_id
    assert "**** **** ****" in get_response.json()["card_number"]
