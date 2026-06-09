FROM ubuntu:24.04

# Prevent interactive prompts from halting the build process
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    libgl1 \
    libglib2.0-0 \
    libx11-6 \
    && rm -rf /var/lib/apt/lists/*


# Create a virtual environment to avoid Ubuntu's "externally-managed-environment" error
RUN python3 -m venv /opt/venv

# Ensure all subsequent python/pip commands use the virtual environment
ENV PATH="/opt/venv/bin:$PATH"

# Upgrade pip and install Panda3D
RUN pip install --upgrade pip && \
    pip install panda3d panda3d-gltf

# Set the working directory for your project
WORKDIR /app

COPY assets ./assets
COPY src ./src
COPY __init__.py ./__init__.py
COPY main.py ./main.py

# CMD ["python3", "main.py"]