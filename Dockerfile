# Use an official lightweight Python image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /code

# Install system dependencies if needed
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file first to leverage Docker caching
COPY ./requirements.txt /code/requirements.txt

# Install dependencies
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy the rest of your application code
COPY . /code

# Create an explicit database directory and grant full write permissions
RUN mkdir -p /code/data && chmod -R 777 /code

# Command to run the FastAPI app via Uvicorn in production
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "10000"]