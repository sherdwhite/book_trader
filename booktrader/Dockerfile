# Use the official Python image as the base image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/booktrader/
ENV DJANGO_SETTINGS_MODULE=core.settings
ENV DEBUG=True

# Install system dependencies in one layer
# Benefits: Single layer for system packages, cleaned up apt cache
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip install --upgrade pip

# Set working directory
WORKDIR /booktrader

# Copy and install Python dependencies first (better caching)
# Benefits: Dependencies are cached separately from code changes
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
# Benefits: Code changes don't invalidate dependency cache
COPY . .

# Make entrypoint executable
RUN chmod +x entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]
