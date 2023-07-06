# Use a base Python image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the Python script to the container
COPY warmup.py .

# Install any necessary dependencies
RUN pip install requests

# Set the command to execute when the container starts
CMD ["python", "warmup.py"]
