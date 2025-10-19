from django.contrib import admin
from .models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['transaction_id', 'user', 'amount', 'transaction_type', 'is_fraud', 'fraud_probability', 'created_at']
    list_filter = ['is_fraud', 'transaction_type', 'created_at']
    search_fields = ['transaction_id', 'sender_upi', 'receiver_upi', 'user__username']
    readonly_fields = ['transaction_id', 'fraud_probability', 'fraud_details', 'created_at']
    date_hierarchy = 'created_at'
