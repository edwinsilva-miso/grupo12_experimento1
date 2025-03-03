# Use the official Python image from the Docker Hub
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the Pipfile and Pipfile.lock from the /productos service to the working directory
COPY productos/Pipfile productos/Pipfile.lock ./

# Install pipenv and the dependencies
RUN pip install pipenv && pipenv install --deploy --ignore-pipfile

# Copy the rest of the application code from the /productos service to the working directory
COPY productos/ ./

# Expose the port the app runs on
EXPOSE 5000

# Define the command to run the application
CMD ["pipenv", "run", "flask", "run", "--host=0.0.0.0"]