# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY  pr_requests.py requirements.txt /app/

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Set default environment variables (can be overridden at runtime)
ENV REPO_OWNER=octocat
ENV REPO_NAME=Hello-World

# Run the application
CMD ["python", "github_pr_summary.py"]