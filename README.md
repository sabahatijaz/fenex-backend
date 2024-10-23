backend
cd Docker
run ./launch_db.sh
run docker cp init-db.sh fenex-fastapi-postgres:/init-db.sh
run docker exec -it fenex-fastapi-postgres bash /init-db.sh
run ./launch_dev.sh
run ./run_migration.sh
## Getting Started


Follow these steps to set up the environment and run the application:

1. **Clone the repository**:
   ```
   git clone https://github.com/sabahatijaz/fenex-backend.git
   ```



2. **Navigate to the Docker directory**:
   ```
   cd Docker
   ```

3. **Launch the database**:
   ```
   ./launch_db
   ```

4. **Start the Redis cache**:
   ```
   ./launch_redis
   ```

5. **Setup the database**:
   - Open the `DATABASE` file and follow the instructions to create the database and initial users.

6. **Launch the development environment**:
   ```
   ./launch_dev
   ```

7. **Run database migrations**:
   ```
   ./make_migrations
   ```

8. **Connect to the backend container**:
   ```
   docker exec -it fenex-fastapi-dev bash
   ```

9. **Execute tests**:
   - Navigate to the test directory and run the test suite:
     ```
     cd test
     python main
     ```
   - Confirm that all tests pass as expected.