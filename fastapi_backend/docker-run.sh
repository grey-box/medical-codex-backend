# Stop and remove existing containers

docker stop fastapi_backend
docker rm fastapi_backend

# This program launches fastapi_backend in a local docker container.

docker run -p 8080:8080 \
  --env-file ".env" \
  --name fastapi_backend \
  --volume ./database:/app/database \
  --network host \
  local/fastapi-backend
