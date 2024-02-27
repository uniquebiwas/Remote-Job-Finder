# Stage 1: Build
FROM python:3.9-alpine AS builder

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app

COPY . /app

# Install dependencies
RUN apk --no-cache add build-base && \
    pip install --no-cache-dir -r requirements.txt

# Stage 2: Production
FROM nginx:alpine

COPY --from=builder /app /app

# Remove default Nginx configuration
RUN rm -v /etc/nginx/nginx.conf

# Copy custom Nginx configuration
COPY app/nginx/nginx.conf /etc/nginx/

# Copy Django static files
RUN python manage.py collectstatic --noinput

# Expose port 80
EXPOSE 80

# CMD to start Nginx
CMD ["nginx", "-g", "daemon off;"]
