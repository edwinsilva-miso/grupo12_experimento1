# Use the official Python image from the Docker Hub
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Install pipenv
RUN pip install --no-cache-dir pipenv

# Copy the Pipfile and Pipfile.lock from the /ccp_web_bff directory to the working directory
COPY ccp_web_bff/Pipfile ccp_web_bff/Pipfile.lock ./

# Install the dependencies
RUN pipenv install --deploy --ignore-pipfile

# Copy the rest of the application code from the /ccp_web_bff directory to the working directory
COPY ccp_web_bff/ ./

# Expose the port the app runs on
EXPOSE 5001

# Command to run the application
CMD ["pipenv", "run", "flask", "run", "--host=0.0.0.0"]