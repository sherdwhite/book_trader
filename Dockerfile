# Use the official Python image as the base image
FROM python:3.11.2

# Set working directory for the Django project
WORKDIR /oreilly_code_challenge/

# Set environment variables for Django
ENV PYTHONPATH /oreilly_code_challenge/
ENV DJANGO_SETTINGS_MODULE voltronflamingo.settings

# Copy the entire project to the container
COPY . /oreilly_code_challenge/

# Install Python dependencies
RUN pip install -r /oreilly_code_challenge/requirements.txt

# Install Node.js and npm
RUN apt-get update
RUN apt-get install -y nodejs npm --fix-missing

# Change working directory to the static folder where the React app is located
WORKDIR /oreilly_code_challenge/static

# Install frontend dependencies
RUN npm install

# Install webpack globally
RUN npm install -g webpack webpack-cli

# Build the React app
RUN npm run build

# Switch back to the main working directory
WORKDIR /oreilly_code_challenge/

# Command to start both Django and React
CMD ["./manage.py", "runserver", "0.0.0.0:8000"]
