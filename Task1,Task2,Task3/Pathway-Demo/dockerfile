# Use official Python base image
FROM python:3.10-slim

# Set working directory inside container
WORKDIR /app

# Copy project files
COPY requirement.txt .
RUN pip install --no-cache-dir -r requirement.txt


COPY . .

# Run the app
CMD ["python", "app1.py"]
