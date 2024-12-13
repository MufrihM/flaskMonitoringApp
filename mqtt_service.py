import paho.mqtt.client as mqtt
from threading import Thread, current_thread
# from flask import current_app


# MQTT Callback functions
def on_connect(client, userdata, flags, rc):
    """Callback when connected to MQTT broker."""
    app = userdata
    with app.app_context():
        topic1 = app.config["MQTT_TOPIC1"]
        topic2 = app.config["MQTT_TOPIC2"]
        print(f"Subscribed to topics: {topic1}, {topic2}")
        client.subscribe([(topic1, 1), (topic2, 1)])
        print("Connected to MQTT Broker!")

def on_message(client, userdata, msg):
    """Callback when a message is received."""
    print(f"Message received on thread:{current_thread().name}")
    app = userdata
    with app.app_context():
        payload = msg.payload.decode() # menerjemahkan pesan yang diterima
        print(f"Received message: {payload} on topic {msg.topic}")
        
        # Koneksi ke mongodb untuk penyimpanan data
        db = app.config["MONGO_CLIENT"].db

        # Penyimpanan data ke database sesuai dengan topik
        topic1 = app.config["MQTT_TOPIC1"]
        topic2 = app.config["MQTT_TOPIC2"]

        if msg.topic == topic1:
            db.temp.insert_one({
            "topic": msg.topic,
            "message": payload,
            "timestamp": app.config.get("timestamp_func")()
            })
        elif msg.topic == topic2:
            db.humid.insert_one({
            "topic": msg.topic,
            "message": payload,
            "timestamp": app.config.get("timestamp_func")()
            })
        

# Initialize MQTT Client
def start_mqtt(app):
    mqtt_client = mqtt.Client()

    mqtt_client.user_data_set(app)

    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message

    broker = app.config["MQTT_BROKER"]
    port = app.config["MQTT_PORT"]

    """Start MQTT client in a separate thread."""
    try:
        mqtt_client.connect(broker, port, 60)
        mqtt_thread = Thread(target=mqtt_client.loop_forever, daemon=True, name="MQTTThread")
        mqtt_thread.start()
        print(f"Started MQTT Thread: {mqtt_thread.name}")
    except Exception as e:
        print(f"Error connecting to MQTT Broker: {e}")
