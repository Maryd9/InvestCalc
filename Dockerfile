FROM python:3.9.7-slim

ENV PYTHONBUFFERED 1

WORKDIR /app
COPY requirements.txt /app
RUN pip install -r requirements.txt

COPY . /app
EXPOSE 5000
