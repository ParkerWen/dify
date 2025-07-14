# MinerU API Server

This directory contains the MinerU API server, which provides document parsing and analysis capabilities via a FastAPI application. It supports PDF, Office, and image file parsing, with optional GPU acceleration.

## Features

- Parse and analyze PDF, Office, and image files
- REST API powered by FastAPI
- Supports local and S3 file sources
- Outputs structured data (JSON, Markdown)
- GPU support via NVIDIA Docker

## Quick Start

### 1. Build and Run with Docker Compose

Add the following service definition to your `docker-compose.yaml`:

```yaml
  # The MinerU API.
  mineru-api:
    build:
      context: ./mineru-api
      args:
        - PIP_MIRROR_URL=${PIP_MIRROR_URL:-}
    restart: always
    ports:
      - "${MINERU_API_PORT:-8000}:8000"
    deploy:
      resources:
        reservations:
          devices:
            - driver: "nvidia"
              count: "all"
              capabilities: ["gpu"]
```

### 2. Build and Run Manually

```bash
docker build -t mineru-api .
docker run --gpus all -p 8000:8000 mineru-api
```

### 3. API Usage

The main endpoint is `/file_parse`, which accepts file uploads or file paths and returns parsed results.

## Requirements

- Python 3.10 (for development)
- Docker (for containerized deployment)
- NVIDIA GPU and drivers (for GPU acceleration)

Python dependencies (see `requirements.txt`):

- magic-pdf[full]
- modelscope
- fastapi
- uvicorn
- python-multipart

## File Structure

- `app.py` - FastAPI application
- `Dockerfile` - Container build instructions
- `entrypoint.sh` - Container entrypoint script
- `requirements.txt` - Python dependencies
- `magic-pdf.json` - Configuration for PDF parsing
- `models/` - Model files
- `layoutreader/` - Layout reader utilities

## Notes

- The API exposes port 8000 by default.
- GPU is recommended for best performance.
- For more details, see the code and comments in `app.py`.
