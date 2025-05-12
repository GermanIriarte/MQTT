FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y iputils-ping

COPY grpc_client.py .
COPY health_pb2.py .
COPY health_pb2_grpc.py .

ENV PYTHONUNBUFFERED=1


CMD ["python", "grpc_client.py"]
