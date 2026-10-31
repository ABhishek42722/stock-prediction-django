from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

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


class Prediction(models.Model):
    THRESHOLD_CHOICES = [(3, "3%"), (5, "5%"), (7, "7%"), (9, "9%")]

    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name="predictions")
    threshold = models.PositiveSmallIntegerField(choices=THRESHOLD_CHOICES)
    probability = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(1.0)])
    predicted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-predicted_at"]
        constraints = [
        models.CheckConstraint(
            condition=models.Q(probability__gte=0, probability__lte=1),
            name="probability_between_0_and_1",
        )
        ]
    def __str__(self):
        return f"{self.stock.symbol}: {self.probability:.0%} chance of a atleast a {self.threshold}% rise"