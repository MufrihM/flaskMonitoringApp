import os
# from dotenv import load_dotenv
from dotenv import load_dotenv

load_dotenv()

class Config:
    MONGO_URI = os.getenv("MONGO_URI")
    SECRET_KEY = os.getenv("SECRET_KEY")
    MQTT_BROKER = os.getenv("MQTT_BROKER")
    MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))
    MQTT_TOPIC1 = os.getenv("MQTT_TOPIC1")
    MQTT_TOPIC2 = os.getenv("MQTT_TOPIC2")