# Text-to-Image Generator with Docker Compose (CPU Version)

This project provides a simple text-to-image generation service using a small model, with a user-friendly web interface, all running in Docker containers. This version is optimized for systems without NVIDIA GPUs.

## Prerequisites

- Docker and Docker Compose installed on your system
- At least 8GB of RAM (16GB recommended)

## Project Structure

```
text-to-image-app/
├── docker-compose.yml
├── model/
│   ├── Dockerfile
│   ├── model_server.py
│   └── requirements.txt
└── frontend/
    ├── Dockerfile
    ├── package.json
    ├── index.html
    └── app.js
```

## Getting Started

1. Clone this repository or create the file structure as shown above.

2. Build and start the containers:

```bash
docker-compose up --build
```

3. Access the web interface at [http://localhost:3000](http://localhost:3000)

## Configuration

- The default model is "runwayml/stable-diffusion-v1-5" which is smaller and better suited for CPU
- You can change the model by modifying the `MODEL_NAME` environment variable in the docker-compose.yml
- The application is configured to run on CPU

## Stopping the Application

```bash
docker-compose down
```

## Notes

- The first time you run this, it will download the AI model which might take some time
- Image generation will be slower on CPU (expect 30-60 seconds per image)
- Reduce the image size (width and height) in the UI for faster generation
- Consider using fewer inference steps (1-3) for quicker results
- The generated models are cached in a Docker volume for faster loading on subsequent runs

## Port Configuration

- The model service runs on port 8080 (http://localhost:8080)
- The frontend UI runs on port 3000 (http://localhost:3000)

If you still encounter port conflicts, you can change these in the docker-compose.yml file.