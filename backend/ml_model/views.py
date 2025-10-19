from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .fraud_detector import FraudDetector
from transactions.models import Transaction


class TestFraudDetectionView(APIView):
    """
    API endpoint to test fraud detection on an existing transaction
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        transaction_id = request.data.get('transaction_id')
        
        if not transaction_id:
            return Response(
                {'error': 'transaction_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            transaction = Transaction.objects.get(
                id=transaction_id,
                user=request.user
            )
        except Transaction.DoesNotExist:
            return Response(
                {'error': 'Transaction not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Run fraud detection
        detector = FraudDetector()
        result = detector.predict(transaction)
        
        return Response(result, status=status.HTTP_200_OK)


class ModelStatusView(APIView):
    """
    API endpoint to check model status
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        detector = FraudDetector()
        
        return Response({
            'model_loaded': detector.model is not None and detector.model.model is not None,
            'detection_method': 'cnn_model' if detector.model and detector.model.model else 'rule_based',
            'status': 'operational'
        })
