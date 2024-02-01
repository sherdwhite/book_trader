# Use the official Python image as the base image
FROM python:3.11.2

# Upgrade to the latest version of pip
RUN pip install --upgrade pip

# Set environment variables for Django
ENV PYTHONPATH /oreilly_code_challenge/backend/
ENV DJANGO_SETTINGS_MODULE voltronflamingo.settings

# Copy the entire project to the container
COPY . /backend

# Set working directory for the Django project
WORKDIR /backend

# Install Python dependencies
RUN pip install -r requirements.txt

# Command to start both Django and React
CMD ["./manage.py", "runserver", "0.0.0.0:8000"]
