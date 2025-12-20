# Use a lightweight base image
FROM python:slim

# Create a non-root user for security
RUN useradd -m appuser

# Set the working directory
WORKDIR /app

# Install flask
RUN pip install flask

# Copy the application code (assuming there is app.py or similar, but for this exercise we just prepare the environment)
# COPY . .

# Switch to the non-root user
USER appuser

# Expose the port (though deployment handles this, it's good practice)
EXPOSE 3000

# Command to run the app (placeholder as app code is not provided in detail)
# Assuming the app is named app.py and listens on port 3000
CMD ["python", "app.py"]
