"""
ASGI config for UPI Fraud Detection project.
"""
import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'upi_fraud_detection.settings')
application = get_asgi_application()
