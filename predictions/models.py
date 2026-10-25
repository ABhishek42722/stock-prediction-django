from django.db import models

# Create your models here.
class Stock(models.Model):
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=10)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["symbol", "date"], name="unique_symbol_date"),
        ]

    def __str__(self):
        return f"{self.name} ({self.symbol}) - {self.price} on {self.date}"