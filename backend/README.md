# UPI Fraud Detection - Backend

Django REST Framework backend for UPI Fraud Detection system with CNN-based machine learning.

## Features

- User authentication with JWT
- Transaction management
- Real-time fraud detection using CNN
- Dashboard statistics and analytics
- Fraud alerts system

## Setup

1. Create virtual environment:

```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Setup environment variables:

```bash
copy .env.example .env
# Edit .env with your configuration
```

4. Run migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

5. Create superuser:

```bash
python manage.py createsuperuser
```

6. Run development server:

```bash
python manage.py runserver
```

## API Endpoints

### Authentication

- POST `/api/auth/register/` - Register new user
- POST `/api/auth/login/` - Login user
- POST `/api/auth/token/refresh/` - Refresh access token
- GET `/api/auth/profile/` - Get user profile
- POST `/api/auth/logout/` - Logout user

### Transactions

- GET `/api/transactions/` - List user transactions
- POST `/api/transactions/` - Create new transaction
- GET `/api/transactions/{id}/` - Get transaction details
- GET `/api/transactions/alerts/` - Get fraud alerts
- GET `/api/transactions/stats/` - Get dashboard statistics

### ML Model

- POST `/api/ml/test/` - Test fraud detection
- GET `/api/ml/status/` - Check model status

## Training the CNN Model

```bash
cd ml_model
python cnn_model.py
```

This will create `fraud_detection_cnn.h5` and `scaler.pkl` files.

## Project Structure

```
backend/
├── accounts/          # User authentication
├── transactions/      # Transaction management
├── ml_model/         # ML fraud detection
├── upi_fraud_detection/  # Project settings
└── manage.py
```
