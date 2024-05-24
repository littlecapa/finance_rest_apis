from fastapi import FastAPI
from fastapi.testclient import TestClient
import sys
import os

# Ensure the root directory is in the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import app

client = TestClient(app)

def test_get_stock_price():
    response = client.get("/stock_price/AAPL")
    assert response.status_code == 200
    data = response.json()
    assert "symbol" in data
    assert data["symbol"] == "AAPL"

def test_stock_not_found():
    response = client.get("/stock_price/INVALID")
    assert response.status_code == 404
    assert response.json() == {"detail": "Stock not found"}
