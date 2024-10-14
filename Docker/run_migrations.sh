#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Variables
CONTAINER_NAME="fenex-fastapi-postgres"  # Change to your actual container name
APP_DIR=" ../app"  # Adjust the path if your app directory differs

# Function to run Alembic commands inside the Docker container interactively
run_migrations() {
  echo "Running Alembic migrations interactively in the container: $CONTAINER_NAME..."

  docker exec "$CONTAINER_NAME" bash -c "
    cd $APP_DIR &&
    echo 'Running alembic upgrade head...' &&
    alembic upgrade head &&
    echo 'Creating new migration...' &&
    alembic revision --autogenerate -m 'create users table' &&
    echo 'Running alembic upgrade head again...' &&
    alembic upgrade head
  "

  echo "Migrations completed successfully."
}

# Check if the container is running
if [ "$(docker ps -q -f name=$CONTAINER_NAME)" ]; then
  run_migrations
else
  echo "Error: Container $CONTAINER_NAME is not running. Please start the container and try again."
  exit 1
fi
