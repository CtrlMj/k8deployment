FROM python:3.9.21-slim
WORKDIR /app
COPY serving_requirements.txt .
RUN pip install -r serving_requirements.txt
COPY ["gateway.py", "proto.py", "."]
EXPOSE 9696
ENTRYPOINT ["gunicorn", "--bind=0.0.0.0:9696", "gateway:app"]