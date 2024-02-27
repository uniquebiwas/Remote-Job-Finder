# Stage 1: Build
FROM python:3.9-alpine AS build

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /usr/src/app

COPY . /usr/src/app

# Install dependencies
RUN apk --no-cache add build-base && \
    pip install --no-cache-dir -r requirements.txt

# Collect static files
RUN python manage.py collectstatic --noinput

# Stage 2: Production
FROM nginx:alpine

# Copy the static files collected by Django
COPY --from=build /usr/src/app/staticfiles /usr/share/nginx/html

# Expose port 80 for the Nginx server
EXPOSE 80

# The default command to start Nginx when the container runs
CMD ["nginx", "-g", "daemon off;"]
