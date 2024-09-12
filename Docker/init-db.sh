#!/bin/bash

# Variables
DB_NAME="fastapi"
DB_USER="fenex"
DB_PASS="fenex" # Set the password for the 'fenex' user here
DB_HOST="localhost"
DB_PORT="5432"

# Function to check if a database exists
database_exists() {
    psql -U postgres -h $DB_HOST -p $DB_PORT -lqt | cut -d \| -f 1 | grep -w $DB_NAME > /dev/null
}

# Function to check if a user exists
user_exists() {
    psql -U postgres -h $DB_HOST -p $DB_PORT -tAc "SELECT 1 FROM pg_roles WHERE rolname='$DB_USER'" | grep -q 1
}

# Function to create a database
create_database() {
    echo "Creating database $DB_NAME..."
    psql -U postgres -h $DB_HOST -p $DB_PORT -c "CREATE DATABASE $DB_NAME;"
}

# Function to create a user
create_user() {
    echo "Creating user $DB_USER..."
    psql -U postgres -h $DB_HOST -p $DB_PORT -c "CREATE USER $DB_USER WITH PASSWORD '$DB_PASS';"
    psql -U postgres -h $DB_HOST -p $DB_PORT -c "ALTER USER $DB_USER WITH SUPERUSER;"
}

# Function to grant privileges
grant_privileges() {
    echo "Granting privileges..."
    psql -U postgres -h $DB_HOST -p $DB_PORT -c "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;"
}

# Main script
echo "Starting setup..."

# Check if the user exists; if not, create the user
if ! user_exists; then
    create_user
else
    echo "User $DB_USER already exists."
fi

# Check if the database exists; if not, create the database and grant privileges
if ! database_exists; then
    echo "Database $DB_NAME does not exist."
    create_database
    grant_privileges
else
    echo "Database $DB_NAME already exists."
fi

echo "Setup completed."
