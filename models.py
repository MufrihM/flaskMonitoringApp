from flask_pymongo import ObjectId


def user_serializer(user) -> dict:
    return{
        "id": str(user["_id"]),
        "username": user["username"],
        "email": user["email"]
    }

def temperature_serializer(temp) -> dict:
    return{
        "id": str(temp["_id"]),
        "message": temp["message"],
        "timeStamp": temp["timeStamp"]
    }

def humidity_serializer(humid) -> dict:
    return{
        "id": str(humid["_id"]),
        "msg": humid["msg"],
        "timeStamp": humid["timeStamp"]
    }

def serialize_list(cursor, serializer_func):
    return [serializer_func(item) for item in cursor]