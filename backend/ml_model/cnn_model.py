"""
CNN Model for UPI Fraud Detection
This module contains the CNN architecture for detecting fraudulent transactions
"""
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, models
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from sklearn.preprocessing import StandardScaler
import joblib


class FraudDetectionCNN:
    """
    Convolutional Neural Network for detecting fraudulent UPI transactions.
    The model transforms transaction features into a 2D format suitable for CNN processing.
    """
    
    def __init__(self, input_shape=(8, 8, 1)):
        """
        Initialize the CNN model
        
        Args:
            input_shape: Shape of input data (height, width, channels)
        """
        self.input_shape = input_shape
        self.model = None
        self.scaler = StandardScaler()
        
    def build_model(self):
        """
        Build the CNN architecture
        """
        model = models.Sequential([
            # First Convolutional Block
            layers.Conv2D(32, (3, 3), activation='relu', input_shape=self.input_shape, padding='same'),
            layers.BatchNormalization(),
            layers.Conv2D(32, (3, 3), activation='relu', padding='same'),
            layers.BatchNormalization(),
            layers.MaxPooling2D((2, 2)),
            layers.Dropout(0.25),
            
            # Second Convolutional Block
            layers.Conv2D(64, (3, 3), activation='relu', padding='same'),
            layers.BatchNormalization(),
            layers.Conv2D(64, (3, 3), activation='relu', padding='same'),
            layers.BatchNormalization(),
            layers.MaxPooling2D((2, 2)),
            layers.Dropout(0.25),
            
            # Third Convolutional Block
            layers.Conv2D(128, (3, 3), activation='relu', padding='same'),
            layers.BatchNormalization(),
            layers.Dropout(0.4),
            
            # Flatten and Dense Layers
            layers.Flatten(),
            layers.Dense(256, activation='relu'),
            layers.BatchNormalization(),
            layers.Dropout(0.5),
            layers.Dense(128, activation='relu'),
            layers.BatchNormalization(),
            layers.Dropout(0.5),
            layers.Dense(64, activation='relu'),
            layers.Dropout(0.3),
            
            # Output Layer
            layers.Dense(1, activation='sigmoid')
        ])
        
        model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=0.001),
            loss='binary_crossentropy',
            metrics=['accuracy', keras.metrics.Precision(), keras.metrics.Recall()]
        )
        
        self.model = model
        return model
    
    def train(self, X_train, y_train, X_val, y_val, epochs=50, batch_size=32):
        """
        Train the CNN model
        
        Args:
            X_train: Training features
            y_train: Training labels
            X_val: Validation features
            y_val: Validation labels
            epochs: Number of training epochs
            batch_size: Batch size for training
        """
        if self.model is None:
            self.build_model()
        
        # Scale the data
        X_train_scaled = self.scaler.fit_transform(X_train.reshape(X_train.shape[0], -1))
        X_val_scaled = self.scaler.transform(X_val.reshape(X_val.shape[0], -1))
        
        # Reshape back to 2D
        X_train_scaled = X_train_scaled.reshape(X_train.shape)
        X_val_scaled = X_val_scaled.reshape(X_val.shape)
        
        # Callbacks
        callbacks = [
            EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True),
            ModelCheckpoint('best_model.h5', monitor='val_loss', save_best_only=True)
        ]
        
        # Train the model
        history = self.model.fit(
            X_train_scaled, y_train,
            validation_data=(X_val_scaled, y_val),
            epochs=epochs,
            batch_size=batch_size,
            callbacks=callbacks,
            verbose=1
        )
        
        return history
    
    def predict(self, X):
        """
        Make predictions on new data
        
        Args:
            X: Input features
            
        Returns:
            Fraud probabilities
        """
        X_scaled = self.scaler.transform(X.reshape(X.shape[0], -1))
        X_scaled = X_scaled.reshape(X.shape)
        return self.model.predict(X_scaled)
    
    def save_model(self, model_path, scaler_path):
        """
        Save the trained model and scaler
        
        Args:
            model_path: Path to save the model
            scaler_path: Path to save the scaler
        """
        self.model.save(model_path)
        joblib.dump(self.scaler, scaler_path)
        print(f"Model saved to {model_path}")
        print(f"Scaler saved to {scaler_path}")
    
    def load_model(self, model_path, scaler_path):
        """
        Load a trained model and scaler
        
        Args:
            model_path: Path to the saved model
            scaler_path: Path to the saved scaler
        """
        self.model = keras.models.load_model(model_path)
        self.scaler = joblib.load(scaler_path)
        print(f"Model loaded from {model_path}")
        print(f"Scaler loaded from {scaler_path}")


def create_synthetic_data(n_samples=10000):
    """
    Create synthetic transaction data for training
    This should be replaced with real transaction data
    
    Args:
        n_samples: Number of samples to generate
        
    Returns:
        X: Feature array
        y: Labels (0: legitimate, 1: fraud)
    """
    np.random.seed(42)
    
    # Generate features
    # Features: amount, hour, day, transaction_type, location_change, device_change, frequency, avg_amount
    X = np.random.randn(n_samples, 64).astype(np.float32)
    
    # Generate labels (10% fraud)
    y = np.random.choice([0, 1], size=n_samples, p=[0.9, 0.1])
    
    # Make fraud transactions have distinct patterns
    fraud_indices = np.where(y == 1)[0]
    X[fraud_indices] += np.random.randn(len(fraud_indices), 64) * 2
    
    # Reshape to 2D format for CNN
    X = X.reshape(-1, 8, 8, 1)
    
    return X, y


if __name__ == "__main__":
    # Example usage
    print("Creating synthetic training data...")
    X, y = create_synthetic_data(10000)
    
    # Split data
    split_idx = int(0.8 * len(X))
    X_train, X_val = X[:split_idx], X[split_idx:]
    y_train, y_val = y[:split_idx], y[split_idx:]
    
    print(f"Training samples: {len(X_train)}, Validation samples: {len(X_val)}")
    
    # Create and train model
    print("Building CNN model...")
    cnn = FraudDetectionCNN()
    cnn.build_model()
    
    print("\nModel Summary:")
    cnn.model.summary()
    
    print("\nTraining model...")
    history = cnn.train(X_train, y_train, X_val, y_val, epochs=30)
    
    # Save model
    cnn.save_model('fraud_detection_cnn.h5', 'scaler.pkl')
    
    print("\nTraining complete!")
