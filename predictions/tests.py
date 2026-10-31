from django.test import TestCase

# Create your tests here.
from datetime import date
from decimal import Decimal

from rest_framework.test import APITestCase

from .models import Stock


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