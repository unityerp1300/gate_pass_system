"""
STEP-BY-STEP SETUP GUIDE
========================
1. Install Python 3.11+ from https://python.org
2. Install MySQL 8.0+ from https://dev.mysql.com/downloads/
3. Create MySQL database:
   CREATE DATABASE gate_pass_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   CREATE USER 'gate_pass_user'@'localhost' IDENTIFIED BY 'YourPassword123';
   GRANT ALL PRIVILEGES ON gate_pass_db.* TO 'gate_pass_user'@'localhost';
   FLUSH PRIVILEGES;
4. cd gate_pass_system
5. python -m venv venv
6. venv\Scripts\activate
7. pip install -r requirements.txt
8. python manage.py makemigrations
9. python manage.py migrate
10. python manage.py createsuperuser
11. python manage.py runserver
12. Open http://127.0.0.1:8000
"""