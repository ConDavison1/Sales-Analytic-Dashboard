# Use a lightweight Python image
FROM python:3.10-slim

# Install PostgreSQL client and required system libraries
RUN apt-get update && apt-get install -y \
    libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy only requirements.txt first (for better caching)
COPY requirements.txt ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all backend files
COPY . .

# Optimize Gunicorn for Cloud Run
CMD ["gunicorn", "-b", "0.0.0.0:8080", "--workers=1", "--threads=1", "--timeout=300", "app:app"]


