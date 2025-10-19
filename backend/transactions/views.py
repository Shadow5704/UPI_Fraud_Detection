from rest_framework import generics, status, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.db.models import Count, Sum, Q
from django.utils import timezone
from datetime import timedelta
from .models import Transaction, FraudAlert
from .serializers import TransactionSerializer, TransactionCreateSerializer, FraudAlertSerializer
from ml_model.fraud_detector import FraudDetector


class TransactionListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['transaction_id', 'sender_upi', 'receiver_upi']
    ordering_fields = ['created_at', 'amount', 'fraud_probability']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return TransactionCreateSerializer
        return TransactionSerializer

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Save transaction
        transaction = serializer.save(user=self.request.user)
        
        # Run fraud detection
        try:
            detector = FraudDetector()
            fraud_result = detector.predict(transaction)
            
            transaction.is_fraud = fraud_result['is_fraud']
            transaction.fraud_probability = fraud_result['fraud_probability']
            transaction.fraud_details = fraud_result
            transaction.save()
            
            # Create fraud alert if detected
            if fraud_result['is_fraud']:
                severity = 'CRITICAL' if fraud_result['fraud_probability'] > 0.9 else 'HIGH'
                FraudAlert.objects.create(
                    transaction=transaction,
                    alert_type='FRAUD_DETECTED',
                    severity=severity,
                    message=f"Fraudulent transaction detected with {fraud_result['fraud_probability']*100:.2f}% probability"
                )
        except Exception as e:
            print(f"Error in fraud detection: {str(e)}")
            # Continue even if fraud detection fails


class TransactionDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TransactionSerializer

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)


class FraudAlertListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FraudAlertSerializer

    def get_queryset(self):
        return FraudAlert.objects.filter(
            transaction__user=self.request.user,
            is_resolved=False
        )


class DashboardStatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        
        # Get time filter
        days = int(request.query_params.get('days', 30))
        start_date = timezone.now() - timedelta(days=days)
        
        transactions = Transaction.objects.filter(user=user, created_at__gte=start_date)
        
        # Calculate statistics
        total_transactions = transactions.count()
        total_amount = transactions.aggregate(total=Sum('amount'))['total'] or 0
        fraud_transactions = transactions.filter(is_fraud=True).count()
        fraud_amount = transactions.filter(is_fraud=True).aggregate(total=Sum('amount'))['total'] or 0
        
        # Get fraud rate by day
        fraud_trend = []
        for i in range(days):
            date = timezone.now() - timedelta(days=i)
            day_transactions = transactions.filter(created_at__date=date.date())
            day_fraud = day_transactions.filter(is_fraud=True).count()
            fraud_trend.append({
                'date': date.date().isoformat(),
                'total': day_transactions.count(),
                'fraud': day_fraud
            })
        
        # Recent transactions
        recent_transactions = TransactionSerializer(
            transactions.order_by('-created_at')[:10],
            many=True
        ).data
        
        # Fraud alerts
        unresolved_alerts = FraudAlert.objects.filter(
            transaction__user=user,
            is_resolved=False
        ).count()
        
        return Response({
            'total_transactions': total_transactions,
            'total_amount': float(total_amount),
            'fraud_transactions': fraud_transactions,
            'fraud_amount': float(fraud_amount),
            'fraud_rate': (fraud_transactions / total_transactions * 100) if total_transactions > 0 else 0,
            'unresolved_alerts': unresolved_alerts,
            'fraud_trend': fraud_trend[::-1],  # Reverse to get chronological order
            'recent_transactions': recent_transactions,
        })
