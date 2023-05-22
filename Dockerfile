# Use the official Python image as the base image
FROM python:3.9-slim

# Set the author label
LABEL maintainer="AJ Sathishkumar <ajsatix@gmail.com>"

# Set the working directory in the container
WORKDIR /app

# Copy the Python script to the container
COPY github_pr_satish.py /app

# Install the required dependencies
RUN pip install requests

# Set the command to run the Python script
CMD ["python", "github_pr_satish.py"]
