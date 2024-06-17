# Create a new network if it doesn't exist

docker network create medical-codex-net

# Stop and remove existing containers

docker stop fastapi_backend
docker rm fastapi_backend

# This program launches fastapi_backend in a local docker container.

docker run -p 8000:8000 --env-file ".env" `
  --name fastapi_backend `
  --volume ./database:/app/database `
  --network medical-codex-net `
  local/fastapi-backend
