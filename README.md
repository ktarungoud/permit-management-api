Permit Management API
This project implements a RESTful backend service for managing residential parking permits, including a background job for automated permit expiration.

Overview
The API allows citizens to apply for permits, and city administrators to approve or revoke them. A key feature is a background task that automatically expires pending permits after 5 minutes.

Functional Requirements
1. Permit Application
POST /permits

Input: name, license_plate, address

Output: JSON of the created permit with status = pending

2. List Permits
GET /permits

Optional Filter: ?status=pending|approved|revoked|expired

3. Approve Permit
POST /permits/{permit_id}/approve

Changes permit status to approved.

4. Revoke Permit
POST /permits/{permit_id}/revoke

Changes permit status to revoked.

Async Requirement (Celery + Beat)
A background job runs every 1 minute using Celery Beat. This task performs the following:

Queries all pending permits.

If any pending permits were created over 5 minutes ago, their status is changed to expired.

Technical Stack
Python 3.x
FastAPI, Flask, or Django (FastAPI preferred)
Async framework support (e.g., async def)
In-memory DB (SQLite preferred)
Celery + Celery Beat (using Redis or RabbitMQ as broker)
Docker and Docker Compose (for app, worker, beat, and broker)
Use Git with meaningful commits
bash

Project Structure
.
- app/
--- main.py        # Entry point for FastAPI app
--- models.py      # Permit model
--- schemas.py     # Pydantic schemas for data validation
--- database.py    # Database setup (e.g., SQLite)
--- crud.py        # Business logic for CRUD operations
--- tasks.py       # Celery async tasks (e.g., auto-expire permits)
--- utils.py       # Any helper functions
- worker/
--- celery_worker.py # Celery worker startup configuration
- docker-compose.yml # Docker Compose configuration for multi-service deployment
- Dockerfile         # Dockerfile for building the application image
- requirements.txt   # Python dependencies
- README.md          # Project README file

Setup Instructions
To get the application up and running using Docker Compose:

Clone the repository:
Bash

git clone <your-repository-url>
cd permit_management_api
Ensure Docker and Docker Compose are installed.

Create a .env file in the project root directory with necessary environment variables, particularly for the Redis broker URL (e.g., REDIS_BROKER_URL=redis://redis:6379/0).

Build and start the services:
Bash

docker compose up -d --build
This command will build the Docker images (if not already built) and start the fastapi_app, celery_worker, celery_beat, and redis_broker services in detached mode.

Verify services are running:

Bash

docker compose ps
You should see app, worker, beat, and redis services all in an "Up" status.

API Usage Examples
The API runs on http://localhost:8000 by default.

1. Apply for a Permit (POST /permits)
Request:

Bash

curl -X POST "http://localhost:8000/permits" \
-H "Content-Type: application/json" \
-d '{
  "name": "John Doe",
  "license_plate": "ABC-123",
  "address": "123 Main St"
}'
Response (example):

JSON

{
  "id": "some_uuid_or_id",
  "name": "John Doe",
  "license_plate": "ABC-123",
  "address": "123 Main St",
  "status": "pending",
  "created_at": "2023-10-27T10:00:00.000Z",
  "updated_at": "2023-10-27T10:00:00.000Z"
}
2. List Permits (GET /permits)
Request (all permits):

Bash

curl "http://localhost:8000/permits"
Request (pending permits):

Bash

curl "http://localhost:8000/permits?status=pending"
Response (example):

JSON

[
  {
    "id": "some_uuid_or_id_1",
    "name": "John Doe",
    "license_plate": "ABC-123",
    "address": "123 Main St",
    "status": "pending",
    "created_at": "2023-10-27T10:00:00.000Z",
  },
  {
    "id": "some_uuid_or_id_2",
    "name": "Jane Smith",
    "license_plate": "XYZ-789",
    "address": "456 Oak Ave",
    "status": "approved",
    "created_at": "2023-10-26T09:30:00.000Z",
  }
]
3. Approve Permit (POST /permits/{permit_id}/approve)
Request:

Bash

curl -X POST "http://localhost:8000/permits/some_uuid_or_id_1/approve"
Response (example):

JSON

{
  "id": "some_uuid_or_id_1",
  "name": "John Doe",
  "license_plate": "ABC-123",
  "address": "123 Main St",
  "status": "approved",
  "created_at": "2023-10-27T10:00:00.000Z",
}
4. Revoke Permit (POST /permits/{permit_id}/revoke)
Request:

Bash

curl -X POST "http://localhost:8000/permits/some_uuid_or_id_2/revoke"
Response (example):

JSON

{
  "id": "some_uuid_or_id_2",
  "name": "Jane Smith",
  "license_plate": "XYZ-789",
  "address": "456 Oak Ave",
  "status": "revoked",
  "created_at": "2023-10-26T09:30:00.000Z",
}
Design Decisions
Architecture: The project follows a microservices-like architecture by separating the FastAPI application, Celery worker, and Celery Beat scheduler into distinct Docker containers. This promotes modularity, scalability, and independent deployment of components.

API Framework: FastAPI was chosen for its modern, asynchronous capabilities, built-in data validation (Pydantic schemas), and automatic interactive API documentation (Swagger UI/ReDoc).

Asynchronous Processing: Celery and Celery Beat are used for handling background tasks, specifically the auto-expiration of permits. This offloads time-consuming operations from the main API thread, ensuring the API remains responsive. Redis serves as a robust message broker for Celery tasks.

Database: SQLite is used as an in-memory database for simplicity and ease of setup, fulfilling the assignment's requirement. For production environments, a more persistent and scalable database like PostgreSQL or MongoDB would be recommended.

Containerization: Docker and Docker Compose provide a consistent development and deployment environment, abstracting away system-level dependencies and simplifying the setup process for other developers.

Project Structure: A clear and logical project structure is adopted, separating concerns into app/ for API logic, worker/ for Celery configuration, and root-level files for Docker and dependencies.

Environment Variables: Configuration is managed via .env files, allowing sensitive information and deployment-specific settings to be easily managed outside of the codebase.
