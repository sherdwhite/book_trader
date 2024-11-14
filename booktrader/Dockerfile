# Use the official Python image as the base image
FROM python:3.12-slim

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

# Manually copy the requirements.txt file
COPY booktrader/requirements.txt /booktrader/requirements.txt

# Install Python dependencies
RUN pip install -r requirements.txt

# Command to start the Django server
CMD ["./manage.py", "runserver", "0.0.0.0:8000"]