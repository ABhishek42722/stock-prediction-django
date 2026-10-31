from rest_framework import serializers
from .models import Stock,Prediction

class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ['id', 'name', 'symbol', 'price', 'date']
    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than zero.")
        return value

class PredictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prediction
        fields = ["id", "stock", "threshold", "probability", "predicted_at"]