import asyncio
import websockets
import json
import paho.mqtt.publish as publish

MQTT_BROKER = "mosquitto"
MQTT_PORT = 1883
MQTT_TOPIC = "salud"

async def handle_connection(websocket):
    print(" Cliente conectado via WebSocket", flush=True)
    try:
        async for message in websocket:
            try:
                data = json.loads(message)
                print(f" Recibido por WebSocket: {data}", flush=True)

                publish.single(
                    topic=MQTT_TOPIC,
                    payload=json.dumps(data),
                    hostname=MQTT_BROKER,
                    port=MQTT_PORT
                )
                print(" Publicado en MQTT desde WebSocket", flush=True)
                await websocket.send(" Datos recibidos y publicados")
            except Exception as e:
                error_msg = f" Error al manejar mensaje: {e}"
                print(error_msg, flush=True)
                await websocket.send(error_msg)
    except websockets.exceptions.ConnectionClosedOK:
        print(" Cliente cerró la conexión correctamente", flush=True)
    except websockets.exceptions.ConnectionClosedError as e:
        print(f" Conexión cerrada inesperadamente: {e}", flush=True)

async def main():
    print(" Gateway WebSocket escuchando en puerto 3003", flush=True)
    # Deshabilita el ping/keepalive para evitar timeouts 1011
    async with websockets.serve(
        handle_connection,
        "0.0.0.0",
        3003,
        ping_interval=None
    ):
        await asyncio.Future()  # bloquea indefinidamente

if __name__ == "__main__":
    asyncio.run(main())
