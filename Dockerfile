# Use an official Python runtime as a parent image
FROM python:3.12

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY ./requirements.txt /app/requirements.txt

# Install dependencies
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# Copy the current directory contents into the container
COPY ./src /app

# Expose port 8000 to the outside world (FastAPI default port)
EXPOSE 15000

# Command to run FastAPI with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "15000", "--root-path", "/alexa/breastfeeding"]
