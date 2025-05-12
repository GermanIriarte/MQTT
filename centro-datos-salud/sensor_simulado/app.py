import requests
import random
import time
from datetime import datetime

GATEWAY_URL = "http://gateway_http:3001/sensores"



def generar_datos():
    return {
        "sensor_id": "sensor01",
        "timestamp": datetime.utcnow().isoformat(),
        "body_temperature": round(random.uniform(36.0, 39.0), 1),
        "heart_rate": random.randint(60, 100),
        "blood_pressure": f"{random.randint(100, 130)}/{random.randint(70, 90)}"
    }

while True:
    data = generar_datos()
    try:
        response = requests.post(GATEWAY_URL, json=data)
        print(f"📤 Enviado: {data} -> Respuesta: {response.status_code}", flush=True)
    except Exception as e:
        print(f"❌ Error al enviar datos: {e}", flush=True)
    time.sleep(5)
