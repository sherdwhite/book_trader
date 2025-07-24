# Use the official Python image as the base image
FROM python:3.12-slim

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Upgrade to the latest version of pip
RUN pip install --upgrade pip

# Set environment variables for Django
ENV PYTHONPATH /booktrader/
ENV DJANGO_SETTINGS_MODULE core.settings
ENV DEBUG=True

# Set working directory for the Django project
WORKDIR /booktrader

# Copy only the requirements.txt file to the container
COPY requirements.txt /booktrader/

# Install Python dependencies
RUN pip install -r requirements.txt

# Copy the rest of the project files to the container
COPY . /booktrader

# List the contents of the /booktrader directory for debugging
RUN ls -l /booktrader

# Make the entrypoint script executable
RUN chmod +x /booktrader/entrypoint.sh

# Set the entrypoint to the entrypoint script
ENTRYPOINT ["/booktrader/entrypoint.sh"]
