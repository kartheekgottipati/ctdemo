"""Tracker urls"""
from rest_framework import routers
from django.contrib.auth import views
from django.urls import path
from tracker.views import (
    AddressViewSet,
    TransactionViewSet,
)

router = routers.SimpleRouter()

router.register(r"addresses", AddressViewSet)
router.register(r"transactions", TransactionViewSet)
urlpatterns = router.urls
