import grpc
import health_pb2
import health_pb2_grpc
from datetime import datetime
import random
import time

def run():
    channel = grpc.insecure_channel("gateway:50051")

    stub = health_pb2_grpc.HealthServiceStub(channel)

    while True:
        data = health_pb2.HealthData(
            sensor_id="sensor01",
            timestamp=datetime.utcnow().isoformat(),
            body_temperature=round(random.uniform(36.0, 39.0), 1),
            heart_rate=random.randint(60, 100),
            blood_pressure=f"{random.randint(100, 130)}/{random.randint(60, 90)}"
        )
        print(f"Enviando: {data}")
        response = stub.SendHealthData(data)
        print(f"Enviado por gRPC → Respuesta: {response.message}")

        time.sleep(3)  # Envía cada 3 segundos

if __name__ == "__main__":
    run()
