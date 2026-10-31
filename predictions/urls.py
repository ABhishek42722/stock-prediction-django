from rest_framework.routers import DefaultRouter
from .views import StockViewSet, PredictionViewSet

router = DefaultRouter()
router.register('stocks', StockViewSet)
router.register('predictions', PredictionViewSet)

urlpatterns = router.urls