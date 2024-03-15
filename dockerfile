# Stage 1: Build
FROM python:3.9-alpine AS build
# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txtbb
RUN pip install -r .\requirements.txt


