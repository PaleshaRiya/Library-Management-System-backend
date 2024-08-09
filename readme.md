# library-management-system

## Overview
BookVista is a web application designed to facilitate the management and distribution of e-books across various sections of an online library. The system enables users to issue, return, and manage e-books efficiently, offering a seamless experience for both users and administrators.

## Features
* User Authentication: Secure user login and registration.
* E-Book Management: Users can browse, issue, return e-books and provide feedback.
* Admin Dashboard: Librarian can add, deleteand update e-books and sections. They can grant and revoke user e-book requests.
* Visual Representation : Librarian can view statistics about active user, distribution of books across sections, requests granted/revoked, etc.
* Search Functionality: Users can search for books by title, author, or section.
* Email Notifications: Users receive notifications reminding them to return the book one day before the returnDate.
* Monthly Report Generation : Librarian receives a monthly report regarding the e-book requests via email.
* Task Scheduling: Background tasks for email notifications and other periodic jobs.
* Data Export: Administrators can export user and book data, which is sent via email.
* Dummy Payment Portal : Users can buy an e-book using a dummy payment portal.

## Create Python virtual environment
```
python3 -m venv env
```

## Activate the environment
```
source env/Scripts/activate
```

## Install requirements
```
pip install -r requirements.txt
```
## Start redis server
```
redis-server
```

## Execute the web application
```
python3 main.py
```

## Start Celery worker
```
celery -A main:celery_app worker -P solo --loglevel INFO
```

## Start the Celery beat scheduler
```
celery -A main:celery_app beat --loglevel INFO
```
 
