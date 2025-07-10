# Use official Python runtime as a parent image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app code
COPY . .

# Expose the port your Flask app runs on (default 5000)
EXPOSE 5000

# Set environment variable for Flask
ENV FLASK_APP=main.py

# Run the app with Gunicorn for production
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "main:app"]
