# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set working directory in container
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . .



# Default command to run the app
CMD ["python", "DataShipper.py"]
