# syntax=docker/dockerfile:1
# escape=`
#Useful to set escape to backtick since \ is dir separator for windows.

FROM python:3.11-slim
LABEL authors="Grey-Box, François Pelletier"

# Install dependancies

RUN apt-get -y update

RUN apt-get -y install postgresql postgresql-contrib libpq-dev gcc

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install -r requirements.txt

# Copy the application code
COPY . .

# Expose the application port
EXPOSE 8000

# Run the Application for Development
#CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# Run the Application for Production
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "-k", "uvicorn.workers.UvicornWorker"]
