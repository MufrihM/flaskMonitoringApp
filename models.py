from flask_pymongo import ObjectId

# Fungsi untuk memformat data dari MongoDB ke bentuk JSON-friendly
def product_serializer(product) -> dict:
    return{
        "id": str(product["_id"]),
        "name": product["name"],
        "price": product["price"]
    }

def user_serializer(user) -> dict:
    return{
        "id": str(user["_id"]),
        "username": user["username"],
        "email": user["email"],
        "name": user["name"]
    }

def order_serializer(order) -> dict:
    return{
        "id": str(order["_id"]),
        "user_id": str(order["user_id"]),
        "product_id": [str(product_id) for product_id in order["product_ids"]],
        "total_amount": order["total_amount"],
        "status": order["status"]
    }

def order_details_serializer(order, user, products) -> dict:
    return{
        "id": str(order["_id"]),
        "user": user_serializer(user),
        "products": [product_serializer(product) for product in products],
        "total_amount": order["total_amount"],
        "status": order["status"]
    }

def temperature_serializer(temp) -> dict:
    return{
        "id": str(temp["_id"]),
        "msg": temp["msg"],
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