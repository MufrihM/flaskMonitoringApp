from flask import request, jsonify
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token
from app import mongo

bcrypt = Bcrypt()

class RegisterAPI(Resource):
    def post(self):
        data = request.json
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")

        # Validasi jika username/email sudah terdaftar
        if mongo.db.users.find_one({"username": username}):
            return jsonify({"message": "Username already exists"}), 400

        # Hash password sebelum disimpan
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # Simpan user ke database
        user_id = mongo.db.users.insert_one({
            "username": username,
            "email": email,
            "password": hashed_password,
            "name": data.get("name", "")
        }).inserted_id

        return jsonify({"message": "User registered successfully", "id": str(user_id)})

class LoginAPI(Resource):
    def post(self):
        data = request.json
        username = data.get("username")
        password = data.get("password")

        # get user data
        user = mongo.db.users.find_one({"username": username})
        # user valid
        if not user:
            return jsonify({"message": "User not found"}), 404
        
        # pass valid
        if not bcrypt.check_password_hash(user["password"], password):
            return jsonify({"message": "invalid password"}), 401
        
        # Buat token JWT
        access_token = create_access_token(identity=str(user["_id"]))
        return jsonify({"message": "Login successful", "access_token": access_token})