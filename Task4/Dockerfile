# Base image
FROM python:3.10-slim

# Prevent Python from buffering stdout/stderr
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Copy files into the container
COPY . /app

# Install dependencies
RUN pip install -r requirement.txt

# Expose Streamlit's default port
EXPOSE 8501

# Streamlit configuration (optional but nice)
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_SERVER_ENABLECORS=false
ENV STREAMLIT_SERVER_ENABLEXsrfProtection=false

# Run the Streamlit app
CMD ["streamlit", "run", "main.py"]
