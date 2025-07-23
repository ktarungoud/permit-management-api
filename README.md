# Permit Management API

This project provides a RESTful backend service for managing residential parking permits, incorporating a background job for automated permit expiration. Citizens can apply for permits, and city administrators can approve or revoke them. A Celery Beat task automatically expires pending permits that have exceeded a specific time limit.

## Features

**Permit Application**: Citizens can submit applications for parking permits.
**Permit Listing**: Retrieve a list of all permits with optional filtering by status (pending, approved, revoked, expired). 
**Permit Approval**: City admins can approve pending permits.
**Permit Revocation**: City admins can revoke permits. 
**Automated Permit Expiration**: A background job runs every minute to expire permits that have been in "pending" status for over 5 minutes. 

## Technical Stack

**Python 3.x** 
**FastAPI**: For building the RESTful API.
**MongoDB Atlas**: Cloud-based NoSQL database for data persistence.
**Motor**: Asynchronous Python driver for MongoDB.
**Celery + Celery Beat**: For asynchronous tasks and scheduled jobs. 
**Redis**: Used as the message broker for Celery.
**Docker & Docker Compose**: For containerization and orchestration of the application, worker, beat, and broker services.

## Project Structure

The project follows a standard structure to organize different components:
permit_management_api
-app
---__init.py__
---crud.py
---database.py
---main.py
---models.py
---README.md
---tasks.py
-worker
---__init.py__
---celery_worker.py
-.env
-.gitignore
-docker-compose.py
-Dockerfile
-README.md
-requirements.txt
