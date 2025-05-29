from flask import Flask, request
import json
import paho.mqtt.publish as publish

app = Flask(__name__)

@app.route("/sensores", methods=["POST"])
def recibir_datos():
    data = request.get_json()
    print("Recibido por HTTP:", data)

    try:
        publish.single(
            topic="salud",
            payload=json.dumps(data),
            hostname="mosquitto",
            port=1883
        )
        print("Publicado en MQTT desde HTTP")
    except Exception as e:
        print(f" Error al publicar MQTT desde HTTP: {e}")

    return {"status": "OK"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3001) 
