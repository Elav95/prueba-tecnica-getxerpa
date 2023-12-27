from django.urls import path, include
from rest_framework import routers
from .views import CategoryViewSet, MerchantViewSet, KeywordViewSet, TransactionViewSet

router = routers.DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'merchants', MerchantViewSet)
router.register(r'keywords', KeywordViewSet)
router.register(r'transactions', TransactionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]