from rest_framework import serializers
from .models import Transaction, FraudAlert


class TransactionSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Transaction
        fields = [
            'id', 'transaction_id', 'user', 'user_username',
            'sender_upi', 'receiver_upi', 'amount', 'transaction_type',
            'description', 'device_id', 'ip_address', 'location',
            'is_fraud', 'fraud_probability', 'fraud_details',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['transaction_id', 'user', 'is_fraud', 'fraud_probability', 'fraud_details', 'created_at', 'updated_at']


class FraudAlertSerializer(serializers.ModelSerializer):
    transaction_details = TransactionSerializer(source='transaction', read_only=True)

    class Meta:
        model = FraudAlert
        fields = ['id', 'transaction', 'transaction_details', 'alert_type', 'severity', 'message', 'is_resolved', 'resolved_at', 'created_at']
        read_only_fields = ['created_at']


class TransactionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = [
            'sender_upi', 'receiver_upi', 'amount', 'transaction_type',
            'description', 'device_id', 'ip_address', 'location'
        ]

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than zero.")
        if value > 100000:
            raise serializers.ValidationError("Amount exceeds maximum transaction limit.")
        return value
