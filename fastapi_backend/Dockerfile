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
COPY database/wikidata_names.csv ./database/
COPY database/codex.db ./database/
COPY database/unique_translation_table_20221027.csv ./database/
COPY routers/*.py ./routers/
COPY func/*.py ./func/
COPY test/*.py ./test/
COPY *.py ./

# Expose the application port
EXPOSE 8000

# Run the application 
#CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# Run the Application for Development w/Auto-Reload
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
