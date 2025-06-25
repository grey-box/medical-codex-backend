# syntax=docker/dockerfile:1
# escape=`
#Useful to set escape to backtick since \ is dir separator for windows.

FROM python:3.12-slim
LABEL authors="Grey-Box, François Pelletier"

# Install dependancies

RUN apt-get -y update && apt-get -y upgrade

RUN apt-get -y install build-essential postgresql-15 postgresql-contrib-15 libpq-dev gcc curl

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install -r requirements.txt

# Copy the application code
COPY ./app/ .

# Expose the application port
EXPOSE 8080

# Run the Application
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port 8080 $UVICORN_RELOAD"]
