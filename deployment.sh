CONTAINER_NAME="file_sharing"
IMAGE_NAME="backend:latest"

# Stop and remove the existing container
echo "Stopping and removing existing container and image"
docker stop $CONTAINER_NAME || true
docker rm $CONTAINER_NAME || true
docker rmi $IMAGE_NAME || true

# Build the Docker image
echo "Building latest Docker Image"
docker build -t $IMAGE_NAME 0


# Run the Docker container
echo "Running Docker container"
docker run  --restart always -d -p 5001:5001  --name $CONTAINER_NAME $IMAGE_NAME