# # Stage 1: Build
# FROM python:3.10-slim AS build

# # Set environment variables to prevent Python from buffering and writing pyc files
# ENV PYTHONUNBUFFERED=1
# ENV PYTHONDONTWRITEBYTECODE=1

# # Set the working directory to /app
# WORKDIR /app

# # Copy only the requirements file to leverage Docker's caching for dependencies
# COPY requirements.txt /app/

# # Install the required Python packages
# RUN pip install --no-cache-dir -r requirements.txt

# # Copy the rest of the application code
# COPY . /app

# # Stage 2: Final Image
# FROM python:3.10-slim  

# # Set environment variables again for the final stage
# ENV PYTHONUNBUFFERED=1
# ENV PYTHONDONTWRITEBYTECODE=1

# # Set the working directory to /app
# WORKDIR /app

# # Copy the application code from the build stage
# COPY --from=build /app /app

# # Expose the port that Django runs on (usually 8000)
# EXPOSE 8000

# # Specify the command to start the Django development server
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]


# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define the command to run your application
CMD ["python","manage.py","runserver","0.0.0.0:8000"]