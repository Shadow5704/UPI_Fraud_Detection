from django.db import models
from django.contrib.auth.models import User
import uuid


class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('SEND', 'Send Money'),
        ('RECEIVE', 'Receive Money'),
        ('REQUEST', 'Request Money'),
    )

    transaction_id = models.CharField(max_length=100, unique=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    
    # Transaction Details
    sender_upi = models.CharField(max_length=100)
    receiver_upi = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES, default='SEND')
    description = models.TextField(blank=True, null=True)
    
    # Location and Device Info
    device_id = models.CharField(max_length=100, blank=True, null=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    
    # Fraud Detection
    is_fraud = models.BooleanField(default=False)
    fraud_probability = models.FloatField(default=0.0)
    fraud_details = models.JSONField(blank=True, null=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"

    def __str__(self):
        return f"Transaction {self.transaction_id} - {self.amount}"


class FraudAlert(models.Model):
    transaction = models.OneToOneField(Transaction, on_delete=models.CASCADE, related_name='alert')
    alert_type = models.CharField(max_length=50)
    severity = models.CharField(max_length=20, choices=(
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
        ('CRITICAL', 'Critical'),
    ))
    message = models.TextField()
    is_resolved = models.BooleanField(default=False)
    resolved_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Fraud Alert"
        verbose_name_plural = "Fraud Alerts"

    def __str__(self):
        return f"Alert for {self.transaction.transaction_id}"
