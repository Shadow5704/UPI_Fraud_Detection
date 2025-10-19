from django.urls import path
from .views import (
    TransactionListCreateView,
    TransactionDetailView,
    FraudAlertListView,
    DashboardStatsView
)

urlpatterns = [
    path('', TransactionListCreateView.as_view(), name='transaction-list-create'),
    path('<int:pk>/', TransactionDetailView.as_view(), name='transaction-detail'),
    path('alerts/', FraudAlertListView.as_view(), name='fraud-alerts'),
    path('stats/', DashboardStatsView.as_view(), name='dashboard-stats'),
]
