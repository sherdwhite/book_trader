# Use the official Python image as the base image
FROM python:3.11-slim

# Upgrade to the latest version of pip
RUN pip install --upgrade pip

# Set environment variables for Django
ENV PYTHONPATH /book-trader/booktrader/
ENV DJANGO_SETTINGS_MODULE booktrader.settings
ENV DEBUG=True

# Copy the entire project to the container
COPY . /app

# Set working directory for the Django project
WORKDIR /app

# Install Python dependencies
RUN pip install -r requirements.txt

# Command to start both Django and React
CMD ["./manage.py", "runserver", "0.0.0.0:8000"]
