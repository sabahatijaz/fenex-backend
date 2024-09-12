#!/bin/bash

# Variables
DB_NAME="fastapi"
DB_USER="postgres"
DB_PASS="datapassword"
DB_HOST="localhost"
DB_PORT="5432"
ALCHEMY_URL="postgresql://$DB_USER:$DB_PASS@$DB_HOST:$DB_PORT/$DB_NAME"

# Function to check if a database exists
database_exists() {
    psql -U $DB_USER -h $DB_HOST -p $DB_PORT -lqt | cut -d \| -f 1 | grep -w $DB_NAME > /dev/null
}

# Function to create a database
create_database() {
    echo "Creating database $DB_NAME..."
    psql -U $DB_USER -h $DB_HOST -p $DB_PORT -c "CREATE DATABASE $DB_NAME;"
}

# Function to run alembic migrations
run_migrations() {
    echo "Running Alembic migrations..."
    alembic upgrade head
}

# Main script
echo "Starting setup..."

# Check if the database exists
if ! database_exists; then
    echo "Database $DB_NAME does not exist."
    create_database
else
    echo "Database $DB_NAME already exists."
fi

# Run Alembic migrations
run_migrations

echo "Setup completed."
