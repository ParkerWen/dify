FROM python:3.10-slim-bookworm

# Set the working directory in the container
WORKDIR /app

# Set the environment variable for pip mirror URL
ARG PIP_MIRROR_URL

# Set environment variables to optimize the Docker image
ENV DEBIAN_FRONTEND=noninteractive \
    LANG=C.UTF-8 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1

# Update the package list and install necessary packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Build Python dependencies
COPY requirements.txt .
RUN PIP_MIRROR_URL="${PIP_MIRROR_URL:-https://pypi.org/simple}" && \
    pip install -i "$PIP_MIRROR_URL" -r requirements.txt

# Copy the layoutreader directory
COPY layoutreader /opt/layoutreader

# Copy the models directory
COPY models /opt/models

# Copy the app and its configuration file
COPY entrypoint.sh /app/entrypoint.sh
COPY magic-pdf.json /root/magic-pdf.json
COPY app.py /app/app.py

# Expose the port that FastAPI will run on
EXPOSE 8000

# Command to run FastAPI using Uvicorn, pointing to app.py and binding to 0.0.0.0:8000
ENTRYPOINT [ "/app/entrypoint.sh" ]
CMD ["--host", "0.0.0.0", "--port", "8000"]
