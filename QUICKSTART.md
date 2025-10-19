# Quick Start Guide - UPI Fraud Detection System

## 🚀 Get Started in 5 Minutes!

### Step 1: Backend Setup (2 minutes)

```bash
# Navigate to backend
cd "c:\Users\John Milton M\UPI Fraud Detection\backend"

# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser (follow prompts)
python manage.py createsuperuser

# Start server
python manage.py runserver
```

✅ Backend running at http://localhost:8000

### Step 2: Frontend Setup (2 minutes)

Open a new terminal:

```bash
# Navigate to frontend
cd "c:\Users\John Milton M\UPI Fraud Detection\frontend"

# Install dependencies
npm install

# Start development server
npm run dev
```

✅ Frontend running at http://localhost:3000

### Step 3: Use the Application (1 minute)

1. Open browser: http://localhost:3000
2. Click "Create Account"
3. Register with your details
4. Login to access dashboard
5. Click "New Transaction" to test fraud detection!

## 🎯 Default Credentials (After creating superuser)

- Username: (what you entered)
- Password: (what you entered)

## 📋 Common Commands

### Backend Commands

```bash
# Activate virtual environment
cd backend
venv\Scripts\activate

# Run server
python manage.py runserver

# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create admin user
python manage.py createsuperuser

# Access admin panel
http://localhost:8000/admin
```

### Frontend Commands

```bash
# Start development
cd frontend
npm run dev

# Build for production
npm run build

# Start production server
npm start
```

## 🔧 Troubleshooting

### Port Already in Use

**Backend (8000):**

```bash
# Find process using port 8000
netstat -ano | findstr :8000

# Kill process (replace PID with actual process ID)
taskkill /PID <PID> /F
```

**Frontend (3000):**

```bash
# Change port in frontend
# Edit package.json and add: "dev": "next dev -p 3001"
```

### Module Not Found

**Backend:**

```bash
pip install -r requirements.txt
```

**Frontend:**

```bash
npm install
```

### Database Issues

```bash
cd backend
python manage.py flush  # Clear database
python manage.py migrate  # Reapply migrations
```

## 🎨 Features You Can Try

1. **Create Transaction**

   - Click "New Transaction" in dashboard
   - Enter details and submit
   - See fraud detection in action!

2. **View Analytics**

   - Check dashboard statistics
   - See fraud trend chart
   - Review recent transactions

3. **Test Fraud Detection**
   - Try unusual amounts (very high/low)
   - Test at odd hours
   - Use round amounts
   - See how the system flags them!

## 📱 Test Scenarios

### Safe Transaction

```
Sender: user@paytm
Receiver: friend@phonepe
Amount: 250.50
Type: SEND
Description: Lunch payment
```

### Potentially Fraudulent

```
Sender: test@upi
Receiver: test@upi  # Same sender/receiver
Amount: 50000  # High amount
Type: SEND
Time: 2 AM  # Unusual time
```

## 🌟 Next Steps

1. Explore the admin panel: http://localhost:8000/admin
2. Create multiple transactions
3. Check fraud alerts
4. View transaction history
5. Customize the CNN model
6. Add more features!

## 📞 Need Help?

- Check the main README.md for detailed documentation
- Review the code comments
- Check Django/Next.js official documentation

## 🎉 Enjoy!

Your UPI Fraud Detection system is now running! Start creating transactions and watch the AI detect fraud in real-time.
