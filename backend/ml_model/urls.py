from django.urls import path
from .views import TestFraudDetectionView, ModelStatusView

urlpatterns = [
    path('test/', TestFraudDetectionView.as_view(), name='test-fraud-detection'),
    path('status/', ModelStatusView.as_view(), name='model-status'),
]
