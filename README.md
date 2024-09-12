backend
cd Docker
run ./launch_db.sh
run docker cp init-db.sh fenex-fastapi-postgres:/init-db.sh
run docker exec -it fenex-fastapi-postgres bash /init-db.sh
run ./launch_dev.sh
