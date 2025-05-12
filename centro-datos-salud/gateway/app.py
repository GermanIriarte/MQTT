import grpc
from concurrent import futures
import time
import health_pb2
import health_pb2_grpc
import json
import paho.mqtt.publish as publish

class HealthService(health_pb2_grpc.HealthServiceServicer):
    def SendHealthData(self, request, context):
        data = {
            "sensor_id": request.sensor_id,
            "timestamp": request.timestamp,
            "body_temperature": request.body_temperature,
            "heart_rate": request.heart_rate,
            "blood_pressure": request.blood_pressure,
        }

        print("📡 Recibido por gRPC:", data, flush=True)

        try:
            publish.single(
                topic="salud",
                payload=json.dumps(data),
                hostname="mosquitto",
                port=1883
            )
            print("📨 Publicado en MQTT desde gRPC", flush=True)
        except Exception as e:
            print(f"❌ Error al publicar MQTT desde gRPC: {e}")

        return health_pb2.Response(status="OK")


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    health_pb2_grpc.add_HealthServiceServicer_to_server(HealthService(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    print("🚀 Servidor gRPC escuchando en el puerto 50051", flush=True)
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
