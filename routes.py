from flask import request, jsonify
from flask_restful import Resource
from models import user_serializer, serialize_list, temperature_serializer, humidity_serializer
from flask_pymongo import ObjectId
from flask_jwt_extended import jwt_required, get_jwt_identity
from auth import RegisterAPI, LoginAPI

class UserListAPI(Resource):
    @jwt_required()
    def get(self):
        # mengambil data user
        from app import mongo
        users = mongo.db.users.find()
        return jsonify(serialize_list(users, user_serializer))
    
class UserAPI(Resource):
    @jwt_required()
    def get(self, user_id):
        try:
            from app import mongo
            # mengambil detail user berdasarkan id
            user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
            if user:
                return jsonify(user_serializer(user))
            return jsonify({"message": "User not found"}), 404
        except Exception as e:
            return jsonify({"message": str(e)}), 500
    def put(self, user_id):
        try:
            from app import mongo
            # ambil data dari request
            data = request.json

            # validasi data
            if not data or not data.get("username") or not data.get("email"):
                return jsonify({"message": "Username and email are required"}), 400
            
            # validasi user
            user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
            if not user:
                return ({"message": "User not found"}), 404

            # update user berdasarkan id
            updateData = {
                "username": data["username"],
                "email": data["email"]
            }

            mongo.db.users.update_one({"_id": ObjectId(user_id)}, {"$set": updateData})
            return ({"message": "User updated"}), 200
        except Exception as e:
            return ({"message": str(e)}), 500

class TemperatureAPI(Resource):
    @jwt_required()
    def get(self):
        from app import mongo
        temperatures = mongo.db.temp.find()
        return jsonify(serialize_list(temperatures, temperature_serializer))
    def post(self):
        from app import mongo
        data = request.json
        temp_id = mongo.db.temp.insert_one({
            "msg": data.get("msg"),
            "timeStamp": data.get("timeStamp")
        }).inserted_id
        return jsonify(temperature_serializer(mongo.db.temp.find_one({"_id": temp_id})))
    
class HumidityAPI(Resource):
    @jwt_required()
    def get(self):
        from app import mongo
        humidity = mongo.db.humid.find()
        return jsonify(serialize_list(humidity, humidity_serializer))
    def post(self):
        from app import mongo
        data = request.json
        humid_id = mongo.db.humid.insert_one({
            "msg": data.get("msg"),
            "timeStamp": data.get("timeStamp")
        }).inserted_id
        return jsonify(humidity_serializer(mongo.db.humid.find_one({"_id": humid_id})))

    
def initialize_routes(api):
    # Daftarkan endpoint ke Flask-RESTful API
    api.add_resource(UserListAPI, '/users')
    api.add_resource(UserAPI, '/users/<user_id>')
    api.add_resource(TemperatureAPI, '/temp')
    api.add_resource(HumidityAPI, '/humid')

    #  Endpoint untuk autentikasi
    api.add_resource(RegisterAPI, '/register')
    api.add_resource(LoginAPI, '/login')