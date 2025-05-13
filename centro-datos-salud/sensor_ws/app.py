import asyncio
import websockets
import random
import json
from datetime import datetime

GATEWAY_WS_URL = "ws://gateway_ws:3003"
RETRY_SECONDS = 5

def generar_datos():
    return {
        "sensor_id": "sensor_ws_1",
        "timestamp": datetime.utcnow().isoformat(),
        "body_temperature": round(random.uniform(36.0, 39.0), 1),
        "heart_rate": random.randint(60, 100),
        "blood_pressure": f"{random.randint(100, 130)}/{random.randint(70, 90)}"
    }

async def enviar_datos():
    while True:
        try:
            async with websockets.connect(GATEWAY_WS_URL, ping_interval=None) as websocket:
                print(" Conectado al gateway WebSocket", flush=True)
                while True:
                    data = generar_datos()
                    try:
                        await websocket.send(json.dumps(data))
                        print(f" Enviado por WS: {data}", flush=True)
                    except websockets.exceptions.ConnectionClosedError as e:
                        # Si el server cierra con 1011, lo capturamos y salimos al reconectar
                        print(f" Conexión cerrada por el servidor: {e}", flush=True)
                        break
                    await asyncio.sleep(5)
        except Exception as e:
            print(f" No pude conectar o la conexión falló: {e}", flush=True)
        print(f" Reintentando en {RETRY_SECONDS} segundos...", flush=True)
        await asyncio.sleep(RETRY_SECONDS)

if __name__ == "__main__":
    asyncio.run(enviar_datos())
