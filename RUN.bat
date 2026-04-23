@echo off
title Unity Cement - ERP System
color 1F
echo.
echo  =====================================================
echo    Unity Cement ERP System
echo    Starting on Local Network...
echo  =====================================================
echo.

:: Step 1 - Activate virtual environment
echo  [1/4] Activating virtual environment...
call z:\myenv\Scripts\activate.bat
if errorlevel 1 (
    echo  ERROR: Virtual environment not found at z:\myenv
    echo  Please run SETUP.bat first.
    pause
    exit /b
)

:: Step 2 - Install / verify dependencies
echo  [2/4] Checking dependencies...
pip install -r requirements.txt --quiet

:: Step 3 - Run migrations
echo  [3/4] Applying database migrations...
python manage.py migrate --run-syncdb 2>nul

:: Step 4 - Start server on LAN
echo  [4/4] Starting server...
echo.
echo  =====================================================
echo.
echo   Access from THIS PC:
echo   http://127.0.0.1:8000
echo.
echo   Access from OTHER PCs on same network:
echo   http://192.168.113.161:8000
echo.
echo   Press CTRL+C to stop the server
echo  =====================================================
echo.

python manage.py runserver 0.0.0.0:8000
pause
