# Use Python 3.11 slim image for AMD64 architecture
FROM --platform=linux/amd64 python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY pdf_outline_extractor.py .

# Create input and output directories
RUN mkdir -p /app/input /app/output

# Make the script executable
RUN chmod +x pdf_outline_extractor.py

# Set the entrypoint
ENTRYPOINT ["python", "pdf_outline_extractor.py"]

