Random Sheet Generator

This project generates random music scores using Python, Music21, and LilyPond. It uses Docker to ensure the environment works consistently across all operating systems

Prerequisites

Docker
Docker Compose

Running

Inside project folder:
docker-compose build              # Build the image
docker-compose run --rm sheetgen  # Run the generator


Output

PDF saved in:
outputs/random_score.pdf

Cleaning Up

docker image prune       # Remove unused images
docker container prune   # Remove stopped containers