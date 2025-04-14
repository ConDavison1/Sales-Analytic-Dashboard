# Use the official Python image.
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Create a working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the rest of the app code
COPY . .

# Tell Cloud Run what port to use
ENV PORT=8080

# Run the app
CMD ["gunicorn", "-b", "0.0.0.0:8080", "wsgi:app"]

