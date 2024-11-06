# Use the official Python image from the Docker Hub
FROM python:3.8-slim
# Install net-tools
RUN apt-get update && apt-get install -y net-tools

# Install PostgreSQL client and development libraries
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Set PYTHONPATH for easier imports
ENV PYTHONPATH=/app

# Copy the requirements file from the parent directory
COPY ../requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy the rest of the application code to the container
COPY ../ /app/
# Specify the command to run on container start
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
