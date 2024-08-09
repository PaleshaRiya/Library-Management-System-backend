# app/tasks/celeryworker.py
from celery import Celery, Task
from flask import Flask
from celery import shared_task
import time
from app.services import CeleryService

celery_service = CeleryService()

def celery_init_app(app: Flask) -> Celery:
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask, broker_connection_retry_on_startup=True)
    celery_app.conf.timezone = 'Asia/Kolkata'
    celery_app.config_from_object(app.config["CELERY"])
    celery_app.set_default()
    app.extensions["celery"] = celery_app
    return celery_app


@shared_task(ignore_result=False)
def hello_world():
    print("Hello Celery")
    
@shared_task(ignore_result=False)
def revoke_access():
    return celery_service.revoke_access()

@shared_task(ignore_result=False)
def send_daily_reminder():
    return celery_service.send_daily_reminder()

@shared_task(ignore_result=False)
def send_monthly_report():
    return celery_service.send_monthly_report()

@shared_task(ignore_result=False)
def export_ebooks_csv():
    return celery_service.export_ebooks_csv()