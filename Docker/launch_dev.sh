#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Variables
IMAGE_NAME="fenex-backend"       # Ensure no extra spaces or incorrect characters here
CONTAINER_NAME="fenex-container"
PORT="8000"
ENV_FILE="../.env"
NETWORK_NAME="host"  # Replace this with your desired network name

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

# Build the Docker image from the parent directory as context
echo "Building Docker image: $IMAGE_NAME..."
docker build -t "$IMAGE_NAME" -f Dockerfile .. || { echo "Failed to build image"; exit 1; }

# Check if a container with the same name exists and stop/remove it
CONTAINER_ID=$(docker ps -aq -f name="$CONTAINER_NAME")

if [ -n "$CONTAINER_ID" ]; then
  echo "Stopping container: $CONTAINER_NAME (ID: $CONTAINER_ID)..."
  docker stop "$CONTAINER_ID" || { echo "Failed to stop container"; exit 1; }

  echo "Removing container: $CONTAINER_NAME (ID: $CONTAINER_ID)..."
  docker rm "$CONTAINER_ID" || { echo "Failed to remove container"; exit 1; }
else
  echo "No existing container found with name: $CONTAINER_NAME"
fi

# Run the Docker container interactively with volume mounts for code hot-reloading
echo "Running Docker container: $CONTAINER_NAME..."
docker run \
  --rm -it \
  --name "$CONTAINER_NAME" \
  --env-file "$ENV_FILE" \
  -p "$PORT:8000" \
  -v $PWD/../app:/app/app \
  "$IMAGE_NAME" || { echo "Failed to run container"; exit 1; }

echo "Docker container is running interactively with code hot-reloading."
