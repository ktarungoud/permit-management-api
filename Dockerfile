# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory in the container
# This means the root of the project will be /app inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose port 8000 for the FastAPI application
EXPOSE 8000

# Default command to run the FastAPI application (overridden by docker-compose)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]