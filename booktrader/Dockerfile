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
ENV DJANGO_SETTINGS_MODULE booktrader.settings
ENV DEBUG=True

# Copy the entire project to the container
COPY . /booktrader

# Set working directory for the Django project
WORKDIR /booktrader

# # List the contents of the /booktrader directory for debugging
# RUN ls -l /booktrader

# Install Python dependencies
RUN pip install -r requirements.txt

# Command to start the Django server
CMD ["./manage.py", "runserver", "0.0.0.0:8000"]