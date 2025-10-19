@echo off
echo ========================================
echo UPI Fraud Detection System - Setup
echo ========================================
echo.

echo [1/5] Setting up Backend...
cd backend

echo Creating virtual environment...
python -m venv venv

echo Activating virtual environment...
call venv\Scripts\activate

echo Installing Python dependencies...
pip install -r requirements.txt

echo Running database migrations...
python manage.py makemigrations
python manage.py migrate

echo.
echo [2/5] Backend setup complete!
echo.
echo ========================================
echo [3/5] Setting up Frontend...
cd ..\frontend

echo Installing Node.js dependencies...
call npm install

echo.
echo [4/5] Frontend setup complete!
echo.
echo ========================================
echo [5/5] Setup Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Create a superuser for Django admin:
echo    cd backend
echo    venv\Scripts\activate
echo    python manage.py createsuperuser
echo.
echo 2. Start the backend server:
echo    cd backend
echo    venv\Scripts\activate
echo    python manage.py runserver
echo.
echo 3. Start the frontend server (in new terminal):
echo    cd frontend
echo    npm run dev
echo.
echo 4. Access the application:
echo    http://localhost:3000
echo.
echo ========================================
echo Press any key to exit...
pause >nul
