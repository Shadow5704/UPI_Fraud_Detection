# Project Structure

```
UPI Fraud Detection/
│
├── backend/                          # Django REST Framework Backend
│   ├── accounts/                     # User authentication app
│   │   ├── models.py                 # UserProfile model
│   │   ├── serializers.py            # User serializers
│   │   ├── views.py                  # Auth views
│   │   └── urls.py                   # Auth endpoints
│   │
│   ├── transactions/                 # Transaction management app
│   │   ├── models.py                 # Transaction & FraudAlert models
│   │   ├── serializers.py            # Transaction serializers
│   │   ├── views.py                  # Transaction views & stats
│   │   └── urls.py                   # Transaction endpoints
│   │
│   ├── ml_model/                     # Machine Learning app
│   │   ├── cnn_model.py              # CNN model architecture
│   │   ├── fraud_detector.py         # Fraud detection interface
│   │   ├── views.py                  # ML API views
│   │   ├── urls.py                   # ML endpoints
│   │   └── trained_models/           # Saved models directory
│   │       ├── fraud_detection_cnn.h5
│   │       └── scaler.pkl
│   │
│   ├── upi_fraud_detection/          # Project settings
│   │   ├── settings.py               # Django settings
│   │   ├── urls.py                   # Main URL config
│   │   ├── wsgi.py                   # WSGI config
│   │   └── asgi.py                   # ASGI config
│   │
│   ├── manage.py                     # Django management script
│   ├── requirements.txt              # Python dependencies
│   ├── .env.example                  # Environment variables template
│   ├── .gitignore                    # Git ignore file
│   └── README.md                     # Backend documentation
│
├── frontend/                         # Next.js Frontend
│   ├── app/                          # Next.js App Router
│   │   ├── layout.tsx                # Root layout
│   │   ├── page.tsx                  # Landing page
│   │   ├── globals.css               # Global styles
│   │   ├── login/
│   │   │   └── page.tsx              # Login page
│   │   ├── register/
│   │   │   └── page.tsx              # Registration page
│   │   └── dashboard/
│   │       └── page.tsx              # Dashboard page
│   │
│   ├── context/
│   │   └── AuthContext.tsx           # Authentication context
│   │
│   ├── lib/
│   │   ├── api.ts                    # Axios instance
│   │   ├── auth.ts                   # Auth services
│   │   └── transactions.ts           # Transaction services
│   │
│   ├── public/                       # Static files
│   ├── package.json                  # Node dependencies
│   ├── tsconfig.json                 # TypeScript config
│   ├── tailwind.config.js            # TailwindCSS config
│   ├── postcss.config.js             # PostCSS config
│   ├── next.config.js                # Next.js config
│   ├── .env.local                    # Environment variables
│   ├── .gitignore                    # Git ignore file
│   └── README.md                     # Frontend documentation
│
├── README.md                         # Main project documentation
├── QUICKSTART.md                     # Quick start guide
├── STRUCTURE.md                      # This file
├── setup.bat                         # Windows setup script
└── start.bat                         # Windows start script
```

## Key Components

### Backend Components

#### 1. Authentication System (`accounts/`)

- **UserProfile Model**: Extended user profile with phone and UPI ID
- **JWT Authentication**: Token-based authentication
- **Endpoints**: Register, Login, Profile, Logout

#### 2. Transaction System (`transactions/`)

- **Transaction Model**: Stores transaction details
- **FraudAlert Model**: Stores fraud alerts
- **Dashboard Stats**: Analytics and statistics
- **Endpoints**: CRUD operations, alerts, stats

#### 3. ML System (`ml_model/`)

- **CNN Model**: Deep learning model for fraud detection
- **FraudDetector**: Interface for predictions
- **Feature Engineering**: Extract features from transactions
- **Fallback System**: Rule-based detection when model unavailable

#### 4. Settings (`upi_fraud_detection/`)

- Django configuration
- REST Framework settings
- JWT configuration
- CORS settings
- Database configuration

### Frontend Components

#### 1. Pages (`app/`)

- **Landing Page**: Hero section, features, stats
- **Login Page**: User authentication
- **Register Page**: User registration
- **Dashboard Page**: Main application interface

#### 2. Context (`context/`)

- **AuthContext**: Global authentication state
- User management
- Login/logout functions

#### 3. Services (`lib/`)

- **API Client**: Axios instance with interceptors
- **Auth Service**: Authentication functions
- **Transaction Service**: Transaction operations

#### 4. Styling

- TailwindCSS configuration
- Custom color palette
- Gradient utilities
- Animations

## Data Flow

### Authentication Flow

```
User → Frontend (Login) → API (/api/auth/login/)
    → Backend (Validate) → JWT Token
    → Frontend (Store Token) → Dashboard
```

### Transaction Flow

```
User → Create Transaction → Frontend Form
    → API (/api/transactions/)
    → Backend (Save Transaction)
    → ML Model (Fraud Check)
    → Update Transaction with Result
    → Return to Frontend → Display Result
```

### Fraud Detection Flow

```
Transaction Data → Feature Extraction
    → Reshape for CNN (8x8x1)
    → CNN Model Prediction
    → Fraud Probability
    → Update Transaction
    → Create Alert (if fraud)
```

## Database Schema

### User

- Django's default User model
- Extended with UserProfile

### UserProfile

- user (OneToOne → User)
- phone_number
- upi_id
- timestamps

### Transaction

- user (ForeignKey → User)
- transaction_id (UUID)
- sender_upi
- receiver_upi
- amount
- transaction_type
- device_id
- ip_address
- location
- is_fraud
- fraud_probability
- fraud_details (JSON)
- timestamps

### FraudAlert

- transaction (OneToOne → Transaction)
- alert_type
- severity
- message
- is_resolved
- timestamps

## API Endpoints

### Authentication

- POST `/api/auth/register/`
- POST `/api/auth/login/`
- POST `/api/auth/token/refresh/`
- GET `/api/auth/profile/`
- POST `/api/auth/logout/`

### Transactions

- GET `/api/transactions/`
- POST `/api/transactions/`
- GET `/api/transactions/{id}/`
- GET `/api/transactions/alerts/`
- GET `/api/transactions/stats/`

### ML Model

- POST `/api/ml/test/`
- GET `/api/ml/status/`

## Technology Stack Summary

### Backend

- Python 3.10+
- Django 4.2.7
- Django REST Framework
- TensorFlow/Keras
- PostgreSQL/SQLite
- JWT

### Frontend

- TypeScript
- Next.js 14
- React 18
- TailwindCSS
- Recharts
- Axios

### ML/AI

- TensorFlow
- Keras
- NumPy
- Pandas
- Scikit-learn

## Development Workflow

1. **Backend Development**

   - Create/modify models
   - Run migrations
   - Create/update serializers
   - Implement views
   - Add URL patterns
   - Test endpoints

2. **Frontend Development**

   - Create/modify pages
   - Implement components
   - Add services
   - Style with TailwindCSS
   - Test user flow

3. **ML Development**
   - Prepare training data
   - Train CNN model
   - Save model weights
   - Integrate with backend
   - Test predictions

## Deployment Considerations

- Use PostgreSQL for production
- Set DEBUG=False in production
- Configure proper CORS settings
- Use environment variables for secrets
- Implement proper logging
- Set up SSL/HTTPS
- Configure static file serving
- Optimize CNN model loading
- Implement caching
- Set up monitoring

## Future Enhancements

- WebSocket for real-time updates
- Email notifications
- PDF report generation
- Advanced analytics
- Mobile app
- Model retraining pipeline
- A/B testing framework
- Multi-language support
