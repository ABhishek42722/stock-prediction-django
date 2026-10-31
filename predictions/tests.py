from django.test import TestCase

# Create your tests here.
from datetime import date
from decimal import Decimal

from rest_framework.test import APITestCase

from .models import Stock,Prediction


class StockAPITests(APITestCase):
    def setUp(self):
        self.stock = Stock.objects.create(
            name="Apple Inc",
            symbol="AAPL",
            price=Decimal("190.50"),
            date=date(2026, 10, 24),
        )

    def test_list_stocks(self):
        response = self.client.get("/api/stocks/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_create_stock(self):
        payload = {
            "name": "Adobe Inc",
            "symbol": "ADBE",
            "price": "187.40",
            "date": "2026-10-24",
        }
        response = self.client.post("/api/stocks/", payload, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Stock.objects.count(), 2)
    
    def test_duplicate_symbol(self):
            payload = {
                "name": "Apple Inc",
                "symbol": "AAPL",
                "price": "180.50",
                "date": "2026-10-24",
            }
            response = self.client.post("/api/stocks/", payload, format="json")
            self.assertEqual(response.status_code, 400)
            self.assertEqual(Stock.objects.count(), 1)

    def test_negative_price(self):
        payload = {
            "name": "Negative Price Inc",
            "symbol": "NEG",
            "price": "-100.00",
            "date": "2026-10-24",
        }
        response = self.client.post("/api/stocks/",payload,format="json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Stock.objects.count(), 1)
        self.assertIn("price", response.data)

    def test_history_returns_only_that_stocks_predictions(self):
        other = Stock.objects.create(
            name="Adobe Inc", symbol="ADBE",
            price=Decimal("187.40"), date=date(2026, 10, 24),
        )
        Prediction.objects.create(stock=self.stock, threshold=5, probability=0.7)
        Prediction.objects.create(stock=other, threshold=5, probability=0.3)

        response = self.client.get(f"/api/stocks/{self.stock.id}/predictions/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["stock"], self.stock.id)

    def test_invalid_threshold(self):
        payload = {
            "stock": self.stock.id,
            "threshold": 4,
            "probability": 0.7,
        }
        response = self.client.post("/api/predictions/", payload, format="json")
        self.assertEqual(response.status_code,400)
        self.assertIn("threshold", response.data)
        self.assertEqual(Prediction.objects.count(), 0)

    def test_unknown_stock(self):
        response = self.client.get("/api/stocks/999/predictions/")
        self.assertEqual(response.status_code, 404)

