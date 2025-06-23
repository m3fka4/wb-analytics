# backend/tests/test_api.py

import sys
import os
import pytest
from fastapi.testclient import TestClient


project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir))
sys.path.insert(0, project_root)

from backend.app.main import app

client = TestClient(app)


@pytest.fixture(autouse=True)
def clear_db():
    from backend.app.database import Base, engine
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def test_read_products_empty():
    response = client.get("/api/products/")
    assert response.status_code == 200
    assert response.json() == []


def test_read_products_with_data():
    from backend.app.crud import create_product
    from backend.app.database import SessionLocal
    from backend.app.schemas import ProductCreate

    db = SessionLocal()
    prod_in = ProductCreate(
        name="Тестовый товар",
        price=150.0,
        discounted_price=120.0,
        rating=4.2,
        reviews_count=25
    )
    create_product(db, prod_in)
    db.close()

    params = {"min_price": 100, "max_price": 200, "min_rating": 4, "min_reviews": 10}
    response = client.get("/api/products/", params=params)
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert any(item["name"] == "Тестовый товар" for item in data)

    item = next(item for item in data if item["name"] == "Тестовый товар")
    assert item["price"] == 150.0
    assert item["discounted_price"] == 120.0
    assert item["rating"] == 4.2
    assert item["reviews_count"] == 25