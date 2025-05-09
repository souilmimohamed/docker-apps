# Start with Ubuntu base image
FROM debian:latest

# Avoid prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Update package list and remove unnecessary files
RUN apt-get update && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Command to run when container starts
CMD ["/bin/bash"]
