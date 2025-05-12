import grpc
import time
import random
import datetime
from health_pb2 import HealthData
from health_pb2_grpc import HealthServiceStub

def generar_datos():
    return HealthData(
        sensor_id="sensor01",
        timestamp=datetime.datetime.utcnow().isoformat(),
        body_temperature=round(random.uniform(36.0, 38.5), 1),
        heart_rate=random.randint(60, 100),
        blood_pressure=f"{random.randint(100, 130)}/{random.randint(60, 90)}"
    )

def run():
    with grpc.insecure_channel("gateway:50051") as channel:
        stub = HealthServiceStub(channel)
        while True:
            data = generar_datos()
            response = stub.SendHealthData(data)
            print(f"Enviado por gRPC ➜ Respuesta: {response.status}")
            time.sleep(5)

if __name__ == "__main__":
    run()
