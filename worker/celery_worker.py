from celery import Celery
import os
from dotenv import load_dotenv


load_dotenv()

celery_app = Celery(
    "permit_manager",
    broker=os.getenv("REDIS_BROKER_URL", "redis://redis:6379/0"),
    backend=os.getenv("REDIS_BROKER_URL", "redis://redis:6379/0"), # Backend for storing results (optional but good practice)
    include=["app.tasks"] # Where your Celery tasks are defined
)

#
celery_app.conf.beat_schedule = {
    "auto-expire-permits-every-minute": {
        "task": "app.tasks.auto_expire_permits",
        "schedule": 60.0,
        "args": (),
        "options": {"expires": 300},
    },
}
celery_app.conf.timezone = "CST"
celery_app.conf.broker_connection_retry_on_startup = True