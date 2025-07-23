from motor.motor_asyncio import AsyncIOMotorClient
from pydantic_settings import BaseSettings, SettingsConfigDict
import os
from dotenv import load_dotenv


load_dotenv()

class Settings(BaseSettings):
    # Configure to load from .env file
    # The env_file setting will also help, but load_dotenv() provides more certainty.
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')

    mongodb_url: str
    database_name: str = "permit_db"
    redis_broker_url: str = "redis://redis:6379/0" # Default for Docker internal

settings = Settings()

# Debugging: Print to ensure URL is loaded
print(f"Connecting to MongoDB at: {settings.mongodb_url}")

client = AsyncIOMotorClient(settings.mongodb_url)
db = client[settings.database_name]

def get_database():
    """Dependency to get the MongoDB database object."""
    return db

async def connect_to_mongo():
    """ to test MongoDB connection."""
    try:
        await client.admin.command('ping')
        print("MongoDB Atlas connection successful!")
    except Exception as e:
        print(f"MongoDB Atlas connection failed: {e}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(connect_to_mongo())