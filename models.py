from flask_pymongo import ObjectId
import pytz
from datetime import datetime


def user_serializer(user) -> dict:
    return{
        "id": str(user["_id"]),
        "username": user["username"],
        "email": user["email"]
    }

def temperature_serializer(temp) -> dict:
    timestamp = temp["timestamp"]
    # print("before", timestamp)
    # print(message["temp"])
    if isinstance(timestamp, datetime):
        timestamp = timestamp.astimezone(pytz.timezone('Asia/Jakarta')).isoformat()
        # print("after", timestamp)
    return{
        "id": str(temp["_id"]),
        "message": temp["message"],
        "timestamp": timestamp
    }

def humidity_serializer(humid) -> dict:
    timestamp = humid["timestamp"]
    # print("timestamp", timestamp)
    if isinstance(timestamp, datetime):
        timestamp = timestamp.astimezone(pytz.utc).isoformat()
        # print("timestamp", timestamp)
    return{
        "id": str(humid["_id"]),
        "message": humid["message"],
        "timestamp": timestamp
    }

def serialize_list(cursor, serializer_func):
    return [serializer_func(item) for item in cursor]