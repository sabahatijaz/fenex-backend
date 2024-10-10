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
HOST_PORT=5432  # Port on the host
NEW_CONTAINER_PORT=5433 # Port in the container after modifying postgresql.conf

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

# Run the Docker container with the PGPORT variable set to change the PostgreSQL port on startup
echo "Running Docker container: $CONTAINER_NAME..."
docker run --restart=unless-stopped -d \
  --name "$CONTAINER_NAME" \
  --env-file "$ENV_FILE" \
  -e POSTGRES_PASSWORD="$POSTGRES_PASSWORD" \
  -e PGPORT="$NEW_CONTAINER_PORT" \
  -v "$DATA_VOLUME:/var/lib/postgresql/data" \
  -p "$HOST_PORT:$NEW_CONTAINER_PORT" \
  "$IMAGE_NAME" || { echo "Failed to run container"; exit 1; }

# Wait for the container to initialize
echo "Waiting for PostgreSQL to initialize..."
sleep 10 # Adjust this time if necessary

# Verify if the container is up and running with the correct port
echo "Verifying PostgreSQL port in the container..."
docker exec -it "$CONTAINER_NAME" cat /var/lib/postgresql/data/postgresql.conf | grep port

echo "PostgreSQL is running with port $NEW_CONTAINER_PORT."
