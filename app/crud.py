from motor.motor_asyncio import AsyncIOMotorCollection
from app.models import PermitCreate, PermitInDB, PermitStatus, PyObjectId
from datetime import datetime, timedelta
from typing import List, Optional

async def create_permit(collection: AsyncIOMotorCollection, permit: PermitCreate) -> PermitInDB:
    """Creates a new permit application in the database."""
    permit_data = permit.model_dump()
    permit_data["status"] = PermitStatus.pending.value
    permit_data["created_at"] = datetime.utcnow()
    result = await collection.insert_one(permit_data)
    # Fetch the inserted document to get the full data including _id
    created_document = await collection.find_one({"_id": result.inserted_id})
    if created_document:
        return PermitInDB(**created_document)
    raise ValueError("Failed to create permit.")

async def get_permits(collection: AsyncIOMotorCollection, status: Optional[PermitStatus] = None) -> List[PermitInDB]:
    """Retrieves a list of permits, optionally filtered by status."""
    query = {}
    if status:
        query["status"] = status.value
    permits_cursor = collection.find(query)
    # Convert motor cursor to a list of PermitInDB objects
    permits = [PermitInDB(**doc) async for doc in permits_cursor]
    return permits

async def update_permit_status(collection: AsyncIOMotorCollection, permit_id: str, new_status: PermitStatus) -> Optional[PermitInDB]:
    """Updates the status of a specific permit."""
    try:
        object_id = PyObjectId(permit_id)
    except Exception:
        return None # Invalid permit_id format

    update_result = await collection.update_one(
        {"_id": object_id},
        {"$set": {"status": new_status.value}}
    )

    if update_result.modified_count == 1:
        updated_document = await collection.find_one({"_id": object_id})
        if updated_document:
            return PermitInDB(**updated_document)
    return None

async def expire_pending_permits(collection: AsyncIOMotorCollection):
    """
    Background task logic: changes status of pending permits
    created over 5 minutes ago to 'expired'.
    """
    five_minutes_ago = datetime.utcnow() - timedelta(minutes=5)
    update_result = await collection.update_many(
        {"status": PermitStatus.pending.value, "created_at": {"$lt": five_minutes_ago}},
        {"$set": {"status": PermitStatus.expired.value}}
    )
    print(f"Expired {update_result.modified_count} pending permits.")