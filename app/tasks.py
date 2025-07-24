from celery import Celery
from app.database import get_database # Import get_database here
from app.crud import expire_pending_permits
import asyncio

# Initialize Celery app
celery_app = Celery("permit_manager")

@celery_app.task
def auto_expire_permits():
    """Celery task to automatically expire pending permits."""
    db = get_database()
    permits_collection = db.permits

    asyncio.run(expire_pending_permits(permits_collection))
    print("Celery: Auto-expiration task completed.")