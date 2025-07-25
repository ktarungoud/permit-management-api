from pydantic import BaseModel, Field, BeforeValidator, AfterValidator
from datetime import datetime
from typing import Optional, Annotated, Any
from enum import Enum
from bson import ObjectId # Import ObjectId for MongoDB _id type handling


# Custom type for MongoDB's ObjectId to work with Pydantic v2
def validate_objectid(v: Any) -> ObjectId:
    if isinstance(v, ObjectId):
        return v
    if isinstance(v, str) and ObjectId.is_valid(v):
        return ObjectId(v)
    raise ValueError("Invalid ObjectId")

# Use Annotated to create the Pydantic-compatible ObjectId type
PyObjectId = Annotated[ObjectId, BeforeValidator(validate_objectid)]


class PermitStatus(str, Enum):
    """Enum for possible permit statuses."""
    pending = "pending"
    approved = "approved"
    revoked = "revoked"
    expired = "expired"

class PermitBase(BaseModel):
    """Base model for permit attributes."""
    name: str = Field(..., description="Name of the applicant")
    license_plate: str = Field(..., description="Vehicle license plate number")
    address: str = Field(..., description="Residential address")

class PermitCreate(PermitBase):
    """Model for creating a new permit application."""
    pass

class PermitInDB(PermitBase):
    """Model representing a permit as stored in the database."""
    # Using PyObjectId to handle MongoDB's _id and map it to 'id'
    id: PyObjectId = Field(alias="_id", default_factory=ObjectId) # Use ObjectId directly as default_factory
    status: PermitStatus = Field(default=PermitStatus.pending, description="Current status of the permit")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Timestamp of permit creation (UTC)")

    class Config:
        """Pydantic configuration for the model."""
        arbitrary_types_allowed = True
        json_encoders = { # Still needed for JSON serialization
            ObjectId: str, # Encode ObjectId to string when serializing to JSON
            datetime: lambda dt: dt.isoformat() + "Z" # Encode datetime UTC
        }
        populate_by_name = True # Allows mapping _id to id for convenience