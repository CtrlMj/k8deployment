# Dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY ["ping.py", "requirements.txt", "."]

RUN pip install -r requirements.txt

EXPOSE 9696

ENTRYPOINT ["gunicorn", "--bind=0.0.0.0:9696", "ping:app"]