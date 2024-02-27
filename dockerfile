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
FROM python:3.9-alpine

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app

# Copy the application and dependencies from the builder stage
COPY --from=builder /app /app

# Install additional dependencies if needed (e.g., psycopg2 for PostgreSQL)
# RUN apk --no-cache add postgresql-libs && \
#     pip install --no-cache-dir psycopg2-binary

# Expose port 8000
EXPOSE 8000

# CMD to start the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
