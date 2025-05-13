import json
import psycopg2
import paho.mqtt.client as mqtt

MQTT_BROKER = "mosquitto"
MQTT_PORT = 1883
MQTT_TOPIC = "salud"

DB_HOST = "postgres"
DB_NAME = "centro_salud"
DB_USER = "salud"
DB_PASSWORD = "salud123"

def insertar_en_db(data):
    conn = psycopg2.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO health_readings (sensor_id, timestamp, body_temperature, heart_rate, blood_pressure)
        VALUES (%s, %s, %s, %s, %s)
    """, (
        data["sensor_id"],
        data["timestamp"],
        data["body_temperature"],
        data["heart_rate"],
        data["blood_pressure"]
    ))
    conn.commit()
    cursor.close()
    conn.close()

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(" Conectado al broker MQTT", flush=True)
        client.subscribe(MQTT_TOPIC)
    else:
        print(f" Falló la conexión al broker MQTT. Código: {rc}", flush=True)

def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        print(f"Recibido MQTT: {payload}", flush=True)
        insertar_en_db(payload)
    except Exception as e:
        print(f"Error al procesar mensaje: {e}", flush=True)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_BROKER, MQTT_PORT)
client.loop_forever()
