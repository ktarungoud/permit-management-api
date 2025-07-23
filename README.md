# Permit Management API

This project provides a RESTful backend service for managing residential parking permits, incorporating a background job for automated permit expiration. Citizens can apply for permits, and city administrators can approve or revoke them. A Celery Beat task automatically expires pending permits that have exceeded a specific time limit.

## Features

* [cite_start]**Permit Application**: Citizens can submit applications for parking permits. [cite: 7, 8, 9, 10]
* [cite_start]**Permit Listing**: Retrieve a list of all permits with optional filtering by status (pending, approved, revoked, expired). [cite: 11, 12, 13]
* [cite_start]**Permit Approval**: City admins can approve pending permits. [cite: 14, 15, 16]
* [cite_start]**Permit Revocation**: City admins can revoke permits. [cite: 17, 18, 19]
* [cite_start]**Automated Permit Expiration**: A background job runs every minute to expire permits that have been in "pending" status for over 5 minutes. [cite: 20, 21, 22, 23]

## Technical Stack

* [cite_start]**Python 3.x** [cite: 25]
* [cite_start]**FastAPI**: For building the RESTful API. [cite: 26]
* **MongoDB Atlas**: Cloud-based NoSQL database for data persistence.
* **Motor**: Asynchronous Python driver for MongoDB.
* [cite_start]**Celery + Celery Beat**: For asynchronous tasks and scheduled jobs. [cite: 29]
* [cite_start]**Redis**: Used as the message broker for Celery. [cite: 29]
* [cite_start]**Docker & Docker Compose**: For containerization and orchestration of the application, worker, beat, and broker services. [cite: 30]

## Project Structure

[cite_start]The project follows a standard structure to organize different components: [cite: 33]