# Use the official Node.js image as the base image
FROM node:alpine

# Set working directory for the frontend project
WORKDIR /frontend

# Copy the entire frontend project to the container
COPY . .

# Install dependencies
RUN npm install

# Build and run the frontend project
CMD ["npm", "run", "build"]
