from flask import Flask
from flask_restful import Api
from config import Config
from flask_pymongo import PyMongo
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from routes import initialize_routes
from datetime import datetime
from mqtt_service import start_mqtt
import pytz

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

# initialize Flask-RESTful API
api = Api(app)

# initializes mongodb
mongo = PyMongo(app)
app.config["MONGO_URI"] = Config.MONGO_URI
app.config["MONGO_CLIENT"] = mongo

# initialize jwt
app.config['JWT_SECRET_KEY'] = Config.SECRET_KEY
jwt = JWTManager(app)

# get timestamp
def get_current_timestamp():
    utc_now = datetime.utcnow()
    utc_plus_7 = utc_now.replace(tzinfo=pytz.utc).astimezone(pytz.timezone("Asia/Jakarta"))
    return utc_plus_7

app.config["timestamp_func"] = get_current_timestamp

# initialize routes
initialize_routes(api)

# initializes mqtt
app.config["MQTT_BROKER"] = Config.MQTT_BROKER
app.config["MQTT_PORT"] = Config.MQTT_PORT
app.config["MQTT_TOPIC1"] = Config.MQTT_TOPIC1
app.config["MQTT_TOPIC2"] = Config.MQTT_TOPIC2



if __name__ == "__main__":
    # connect to mongodb
    try:
        mongo.cx.server_info()  # Memeriksa koneksi ke MongoDB
        print("Connected to MongoDB!")
    except Exception as e:
        print(f"MongoDB connection error: {e}")
        raise
    
    start_mqtt(app) 
    
    app.run(debug=False)