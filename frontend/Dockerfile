# Use the official Node.js image as the base image
FROM node:alpine

# Set the working directory in the container to /frontend
WORKDIR /frontend

# Copy the entire project to the container
COPY . .

# Install any needed packages specified in package.json
RUN npm install

# Make port 3000 available to the world outside this container
EXPOSE 3000

# Run the app when the container launches
CMD ["npm", "run", "build"]