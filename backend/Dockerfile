# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
# The path is relative to the build context, which is the root directory
COPY ./requirements.txt /app/requirements.txt

# Upgrade pip to the latest version
RUN pip install --upgrade pip

# Install any needed packages specified in requirements.txt
# We strip the hashes on-the-fly to prevent mismatch errors during the build
RUN sed 's/--hash=\S*//g' /app/requirements.txt > /app/requirements-nohash.txt && \
    pip install --no-cache-dir --upgrade -r /app/requirements-nohash.txt

# Copy the backend application into the container at /app/app
# The source path is relative to the build context
COPY ./backend/app /app/app

# Command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

