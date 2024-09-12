#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Variables
CONTAINER_NAME="fenex-fastapi-postgres"
IMAGE_NAME="postgres:latest"
DATA_VOLUME="fenex_data_propto"
ENV_FILE="../.env"
NETWORK_NAME="host"
POSTGRES_PASSWORD="datapassword" # Set your desired superuser password here

# Ensure .env file exists
if [ ! -f "$ENV_FILE" ]; then
  echo "Error: .env file not found!"
  exit 1
fi

# Create a Docker network if it doesn't exist
if [ -z "$(docker network ls -q -f name="$NETWORK_NAME")" ]; then
  echo "Creating Docker network: $NETWORK_NAME..."
  docker network create "$NETWORK_NAME" || { echo "Failed to create network"; exit 1; }
else
  echo "Network $NETWORK_NAME already exists."
fi

# Check if a container with the same name exists, whether running or stopped, and remove it
EXISTING_CONTAINER=$(docker ps -aq -f name="$CONTAINER_NAME")
if [ -n "$EXISTING_CONTAINER" ]; then
  echo "Stopping and removing existing container: $CONTAINER_NAME..."
  docker stop "$EXISTING_CONTAINER" || { echo "Failed to stop container"; exit 1; }
  docker rm "$EXISTING_CONTAINER" || { echo "Failed to remove container"; exit 1; }
else
  echo "No existing container found with name: $CONTAINER_NAME"
fi

# Run the Docker container
echo "Running Docker container: $CONTAINER_NAME..."
docker run --restart=unless-stopped -d \
  --name "$CONTAINER_NAME" \
  --network "$NETWORK_NAME" \
  --env-file "$ENV_FILE" \
  -e POSTGRES_PASSWORD="$POSTGRES_PASSWORD" \
  -v "$DATA_VOLUME:/var/lib/postgresql/data" \
  "$IMAGE_NAME" || { echo "Failed to run container"; exit 1; }

# Wait for the container to initialize
echo "Waiting for PostgreSQL to initialize..."
sleep 10 # Adjust this time if necessary

# Update pg_hba.conf to use md5 authentication
echo "Updating pg_hba.conf to use md5 authentication..."
docker exec -it "$CONTAINER_NAME" bash -c "sed -i \"s/local   all             all                                     trust/local   all             all                                     md5/\" /var/lib/postgresql/data/pg_hba.conf"

# Restart PostgreSQL to apply changes
echo "Restarting PostgreSQL to apply changes..."
docker restart "$CONTAINER_NAME" || { echo "Failed to restart container"; exit 1; }

echo "PostgreSQL container is running with md5 authentication."
