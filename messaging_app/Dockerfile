# Use the base Python 3.10 image
FROM python:3.10-slim

# environment variables to optimize Python performance in Docker
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . /app/

# Expose the default Django port
EXPOSE 8000

# Run the Django development server
# 0.0.0.0 is used to listen on all interfaces within the container
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
