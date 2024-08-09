Library Management System

python3 -m venv env

source env/bin/activate

redis-server

python3 main.py

celery -A main:celery_app worker --loglevel INFO  

celery -A main:celery_app beat --loglevel INFO  