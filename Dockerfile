# Use the official lightweight Python image
FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Copy application files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the default port
EXPOSE 8080

# Command to run the app
CMD ["python", "app.py"]
