# Multi-stage build for lightweight final image
# Stage 1: Builder stage with build dependencies
FROM python:3.11-alpine AS builder

# Install build dependencies
RUN apk add --no-cache \
    gcc \
    musl-dev \
    postgresql-dev \
    libffi-dev \
    build-base

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Runtime stage - lightweight final image
FROM python:3.11-alpine AS runtime

# Install only runtime dependencies (no build tools)
RUN apk add --no-cache \
    postgresql-client \
    libpq

# Copy virtual environment from builder stage
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Set working directory
WORKDIR /app

# Set Python path to current directory
ENV PYTHONPATH=.

# Copy the entire database directory structure
COPY database/ ./database/

# Copy environment file and entrypoint script
COPY .env ./
COPY entrypoint.sh ./

# Make entrypoint script executable
RUN chmod +x entrypoint.sh

# Set the entrypoint
ENTRYPOINT ["./entrypoint.sh"]