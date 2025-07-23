from celery import Celery
import os
from dotenv import load_dotenv

# Load environment variables from .env file
# This is crucial for Celery worker and beat to pick up MONGODB_URL
load_dotenv()

# Initialize Celery application
# The broker URL comes from .env file or defaults to the internal Docker Redis service
celery_app = Celery(
    "permit_manager",
    broker=os.getenv("REDIS_BROKER_URL", "redis://redis:6379/0"),
    backend=os.getenv("REDIS_BROKER_URL", "redis://redis:6379/0"), # Backend for storing results (optional but good practice)
    include=["app.tasks"] # Where your Celery tasks are defined
)

# Configure Celery Beat schedule
celery_app.conf.beat_schedule = {
    "auto-expire-permits-every-minute": {
        "task": "app.tasks.auto_expire_permits", # The name of the task function
        "schedule": 60.0, # Run every 60 seconds (1 minute) [cite: 21]
        "args": (), # No arguments for this task
        "options": {"expires": 300}, # Task expires after 5 minutes if not started/completed (optional)
    },
}
celery_app.conf.timezone = "UTC" # It's good practice to define a timezone
celery_app.conf.broker_connection_retry_on_startup = True # Important for Docker-compose startup order