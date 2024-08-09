from flask import Flask
from app.db import init_db
from flask_cors import CORS 
from flask_jwt_extended import JWTManager
from app.tasks.celeryworker import celery_init_app
from celery.schedules import crontab

from app.services.email_service import EmailService

email_service = EmailService()

def create_app():
    app = Flask(__name__)
    
    app.config["JWT_SECRET_KEY"] = "super-secret"
    app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/1'
    app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/2'
    app.config['CACHE_TYPE'] = "RedisCache"
    app.config['CACHE_REDIS_HOST'] = "localhost"
    app.config['CACHE_REDIS_PORT'] = 6379
    app.config['CACHE_REDIS_DB'] = 3
    
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USE_SSL'] = True
    app.config['MAIL_USERNAME'] = "paleshariya7@gmail.com"
    app.config['MAIL_PASSWORD'] = "frgd tnsr jxqp wamk"
    
    email_service.init_mail(app)
    
    app.config.from_mapping(
        CELERY=dict(
            broker_url="redis://localhost:6379/1",
            result_backend="redis://localhost:6379/2",
            task_ignore_result=True,
            imports=("app.tasks.celeryworker",), 
            beat_schedule={
                "task-revoke-access": {
                    "task": "app.tasks.celeryworker.revoke_access",
                    "schedule": 10,
                },
                "send-daily-reminder": {
                    "task": "app.tasks.celeryworker.send_daily_reminder",
                    "schedule": crontab(hour=17, minute=0),
                },
                "send-monthly-report": {
                    "task": "app.tasks.celeryworker.send_monthly_report",
                    "schedule": crontab(day_of_month=1, hour=0, minute=0),
                },
            },
        ),
    )

    jwt = JWTManager(app)
    celery_app = celery_init_app(app)
    
    CORS(app, resources={r"/api/*": {"origins": "*", "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"], "allow_headers": ["Content-Type", "Authorization"], "supports_credentials": True}})

    with app.app_context():
        init_db()

    from app.controllers.user_controller import user_bp
    from app.controllers.auth_controller import auth_bp
    from app.controllers.section_controller import section_bp
    from app.controllers.ebook_controller import ebook_bp
    from app.controllers.request_controller import request_bp
    from app.controllers.feedback_controller import feedback_bp
    from app.controllers.healthcheck_controller import healthcheck_bp
    
    app.register_blueprint(user_bp, url_prefix='/api/users')
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(section_bp, url_prefix='/api/section')
    app.register_blueprint(ebook_bp, url_prefix='/api/ebook')
    app.register_blueprint(request_bp, url_prefix='/api/request')
    app.register_blueprint(feedback_bp, url_prefix='/api/feedback')
    app.register_blueprint(healthcheck_bp, url_prefix='/api/healthcheck')
    
    return app, celery_app

app, celery_app = create_app()