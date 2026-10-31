from rest_framework import viewsets
from .models import Stock,Prediction
from .serializers import StockSerializer, PredictionSerializer
from rest_framework.decorators import action
from rest_framework.response import Response

class StockViewSet(viewsets.ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    @action(detail=True, methods=["get"])
    def predictions(self, request, pk=None):
        stock = self.get_object()
        serializer = PredictionSerializer(stock.predictions.all(), many=True)
        return Response(serializer.data)

class PredictionViewSet(viewsets.ModelViewSet):
    queryset = Prediction.objects.all()
    serializer_class = PredictionSerializer
