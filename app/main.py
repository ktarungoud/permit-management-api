from fastapi import FastAPI, Depends, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorCollection
from typing import List, Optional

from app.models import PermitInDB, PermitStatus, PermitCreate # Import models and enums
from app.crud import create_permit, get_permits, update_permit_status
from app.database import get_database, connect_to_mongo # Import connect_to_mongo for startup

app = FastAPI(
    title="Permit Management API",
    description="RESTful backend service for managing residential parking permits.",
    version="1.0.0"
)

# Startup event to verify MongoDB connection
@app.on_event("startup")
async def startup_db_client():
    await connect_to_mongo()
    # You might want to ensure an index exists for efficient queries on created_at and status
    # This requires an active connection, so it's good to do here.
    await get_database().permits.create_index([("status", 1), ("created_at", 1)])
    print("Application startup complete.")


@app.post("/permits", response_model=PermitInDB, status_code=status.HTTP_201_CREATED,
          summary="Apply for a new parking permit")
async def apply_for_permit(
    permit: PermitCreate, # Input validation is handled by Pydantic model
    db_collection: AsyncIOMotorCollection = Depends(lambda: get_database().permits)
):
    """
    Creates a new residential parking permit application.
    The initial status will be 'pending'.
    """
    return await create_permit(db_collection, permit)

@app.get("/permits", response_model=List[PermitInDB],
         summary="List all permits with optional status filtering")
async def list_permits(
    status_filter: Optional[PermitStatus] = None,
    db_collection: AsyncIOMotorCollection = Depends(lambda: get_database().permits)
):
    """
    Retrieves a list of all parking permits.
    Can be filtered by status (pending, approved, revoked, expired).
    """
    return await get_permits(db_collection, status_filter)

@app.post("/permits/{permit_id}/approve", response_model=PermitInDB,
          summary="Approve a specific parking permit")
async def approve_permit(
    permit_id: str,
    db_collection: AsyncIOMotorCollection = Depends(lambda: get_database().permits)
):
    """
    Changes the status of a permit to 'approved'.
    """
    updated_permit = await update_permit_status(db_collection, permit_id, PermitStatus.approved)
    if not updated_permit:
        raise HTTPException(status_code=404, detail="Permit not found or could not be updated")
    return updated_permit

@app.post("/permits/{permit_id}/revoke", response_model=PermitInDB,
          summary="Revoke a specific parking permit")
async def revoke_permit(
    permit_id: str,
    db_collection: AsyncIOMotorCollection = Depends(lambda: get_database().permits)
):
    """
    Changes the status of a permit to 'revoked'.
    """
    updated_permit = await update_permit_status(db_collection, permit_id, PermitStatus.revoked)
    if not updated_permit:
        raise HTTPException(status_code=404, detail="Permit not found or could not be updated")
    return updated_permit

# Health check endpoint (optional but good practice)
@app.get("/health", status_code=status.HTTP_200_OK, summary="Health check endpoint")
async def health_check():
    """
    Checks the health of the API.
    """
    return {"status": "ok", "message": "Permit Management API is running."}