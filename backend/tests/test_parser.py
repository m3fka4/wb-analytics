# backend/tests/test_parser.py

import sys
import os
import pytest
import requests
from unittest.mock import patch


project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir))
sys.path.insert(0, project_root)

from backend.parser.wb_parser import parse_wb
from backend.app.database import SessionLocal, Base, engine
from backend.app.crud import get_products


class DummyResp:
    def __init__(self, products):
        self._products = products

    def raise_for_status(self):
        pass

    def json(self):
        return {"data": {"products": self._products}}


@pytest.fixture(autouse=True)
def reset_db():

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def test_parse_wb_single(monkeypatch):
    dummy_products = [{
        "name": "Dummy",
        "priceU": 12345,
        "salePriceU": 10000,
        "rating": 4.0,
        "feedbacks": 5
    }]


    monkeypatch.setattr(requests, "get", lambda *args, **kwargs: DummyResp(dummy_products))

    parse_wb("dummy", max_pages=1)

    db = SessionLocal()
    prods = get_products(db)
    assert len(prods) == 1

    prod = prods[0]
    assert prod.name == "Dummy"
    # 12345/100 = 123.45
    assert prod.price == pytest.approx(123.45)
    # 10000/100 = 100.00
    assert prod.discounted_price == pytest.approx(100.00)
    assert prod.rating == pytest.approx(4.0)
    assert prod.reviews_count == 5
    db.close()