"""
Fraud Detector - Main interface for fraud detection
"""
import numpy as np
import os
from datetime import datetime
from django.conf import settings
from .cnn_model import FraudDetectionCNN


class FraudDetector:
    """
    Main fraud detection interface that uses the CNN model
    """
    
    def __init__(self):
        self.model = None
        self.load_model()
    
    def load_model(self):
        """
        Load the trained CNN model
        """
        try:
            model_path = settings.ML_MODEL_PATH
            scaler_path = settings.SCALER_PATH
            
            if os.path.exists(model_path) and os.path.exists(scaler_path):
                self.model = FraudDetectionCNN()
                self.model.load_model(str(model_path), str(scaler_path))
                print("Fraud detection model loaded successfully")
            else:
                print("Model files not found. Using rule-based detection.")
                self.model = None
        except Exception as e:
            print(f"Error loading model: {str(e)}")
            self.model = None
    
    def extract_features(self, transaction):
        """
        Extract features from a transaction object
        
        Args:
            transaction: Transaction model instance
            
        Returns:
            Feature array shaped for CNN input
        """
        # Extract basic features
        features = []
        
        # 1. Amount (normalized)
        amount = float(transaction.amount)
        features.append(amount / 100000.0)  # Normalize by max amount
        
        # 2. Transaction type (one-hot encoded)
        type_encoding = {'SEND': 0, 'RECEIVE': 1, 'REQUEST': 2}
        features.append(type_encoding.get(transaction.transaction_type, 0) / 2.0)
        
        # 3. Time features
        hour = transaction.created_at.hour / 23.0
        day_of_week = transaction.created_at.weekday() / 6.0
        features.extend([hour, day_of_week])
        
        # 4. UPI ID features (length and patterns)
        sender_len = len(transaction.sender_upi) / 100.0
        receiver_len = len(transaction.receiver_upi) / 100.0
        features.extend([sender_len, receiver_len])
        
        # 5. Location change (0 if no location, 1 otherwise)
        has_location = 1.0 if transaction.location else 0.0
        features.append(has_location)
        
        # 6. Device ID present
        has_device = 1.0 if transaction.device_id else 0.0
        features.append(has_device)
        
        # Add more features to reach 64 (8x8)
        # These could include: user history, transaction frequency, etc.
        # For now, pad with derived features
        while len(features) < 64:
            # Add some derived features and padding
            if len(features) < 16:
                features.append(amount * hour if len(features) == 8 else 0.0)
            else:
                features.append(0.0)
        
        # Reshape to (8, 8, 1) for CNN
        features = np.array(features[:64]).reshape(1, 8, 8, 1).astype(np.float32)
        return features
    
    def rule_based_detection(self, transaction):
        """
        Simple rule-based fraud detection as fallback
        
        Args:
            transaction: Transaction model instance
            
        Returns:
            dict with fraud detection results
        """
        fraud_score = 0.0
        reasons = []
        
        amount = float(transaction.amount)
        
        # Rule 1: Very high amount
        if amount > 50000:
            fraud_score += 0.3
            reasons.append("High transaction amount")
        
        # Rule 2: Unusual time (late night/early morning)
        hour = transaction.created_at.hour
        if hour < 6 or hour > 22:
            fraud_score += 0.2
            reasons.append("Unusual transaction time")
        
        # Rule 3: Round amounts (often suspicious)
        if amount % 1000 == 0 and amount > 10000:
            fraud_score += 0.15
            reasons.append("Round amount transaction")
        
        # Rule 4: Missing device or location info
        if not transaction.device_id or not transaction.location:
            fraud_score += 0.25
            reasons.append("Missing device/location information")
        
        # Rule 5: Same sender and receiver
        if transaction.sender_upi == transaction.receiver_upi:
            fraud_score += 0.5
            reasons.append("Self-transfer detected")
        
        is_fraud = fraud_score > 0.5
        
        return {
            'is_fraud': is_fraud,
            'fraud_probability': min(fraud_score, 1.0),
            'detection_method': 'rule_based',
            'reasons': reasons,
            'timestamp': datetime.now().isoformat()
        }
    
    def predict(self, transaction):
        """
        Predict if a transaction is fraudulent
        
        Args:
            transaction: Transaction model instance
            
        Returns:
            dict with fraud detection results
        """
        try:
            if self.model is not None and self.model.model is not None:
                # Extract features
                features = self.extract_features(transaction)
                
                # Make prediction
                probability = float(self.model.predict(features)[0][0])
                is_fraud = probability > 0.5
                
                return {
                    'is_fraud': is_fraud,
                    'fraud_probability': probability,
                    'detection_method': 'cnn_model',
                    'confidence': abs(probability - 0.5) * 2,  # 0 to 1 confidence
                    'timestamp': datetime.now().isoformat()
                }
            else:
                # Fallback to rule-based detection
                return self.rule_based_detection(transaction)
                
        except Exception as e:
            print(f"Error in fraud detection: {str(e)}")
            # Fallback to rule-based detection
            return self.rule_based_detection(transaction)
