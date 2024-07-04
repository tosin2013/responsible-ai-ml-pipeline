# Makefile for testing Docker deployment of tutorial_bias_advertising

# Docker image name
IMAGE_NAME := tutorial_bias_advertising

# Build the Docker image
build:
	docker build -t $(IMAGE_NAME) .

# Run tests within the Docker container
test:
	docker run --rm $(IMAGE_NAME) pytest

# Remove Docker images
clean:
	docker rmi $(IMAGE_NAME)

.PHONY: build test clean