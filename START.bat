@echo off
echo ============================================
echo   Unity Cement Gate Pass System - Setup
echo ============================================
echo.

echo [1/5] Creating virtual environment...
python -m venv venv
call venv\Scripts\activate

echo [2/5] Upgrading pip and installing dependencies...
python -m pip install --upgrade pip
pip install --only-binary :all: Pillow
pip install -r requirements.txt

echo [3/5] Running migrations...
python manage.py makemigrations accounts
python manage.py makemigrations internal_pass
python manage.py makemigrations visitor_pass
python manage.py makemigrations dashboard
python manage.py migrate

echo [4/5] Creating superuser (admin/admin123)...
python manage.py shell -c "from accounts.models import Employee; Employee.objects.filter(username='admin').exists() or Employee.objects.create_superuser('admin', 'admin123', employee_name='System Admin', employee_code='ADMIN001', department='Admin', designation='System Administrator', email='admin@unitycement.in', role='admin')"

echo [5/5] Starting server...
echo.
echo ============================================
echo   Open: http://127.0.0.1:8000
echo   Username: admin
echo   Password: admin123
echo ============================================
python manage.py runserver
pause
