# pull official base image
FROM python:3.10.7-slim-buster

# set work directory
WORKDIR /usr/src/app

COPY . .

# set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=app.py
ENV FLASK_DEBUG=True
ENV DATABASE_URL=postgresql://admin:TravelMas2022@34.125.75.3:5432/travel_mas
ENV SQL_HOST=db
ENV SQL_PORT=5432
ENV DATABASE=postgres
ENV GOOGLE_APPLICATION_CREDENTIALS=./gcs-creds.json
ENV GCS_BUCKET=travelmas-bucket

# install system dependencies
RUN apt-get update && apt-get install -y netcat

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

# copy project
COPY . /usr/src/app/

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
