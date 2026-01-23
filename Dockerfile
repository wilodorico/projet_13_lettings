# Use official Python runtime as base image
FROM python:3.12.2-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    DJANGO_SETTINGS_MODULE=oc_lettings_site.settings.production

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Create logs directory
RUN mkdir -p logs

# Make entrypoint script executable
RUN chmod +x entrypoint.sh

EXPOSE 8000

# Use entrypoint script
ENTRYPOINT ["./entrypoint.sh"]
