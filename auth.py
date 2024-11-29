from flask import request, jsonify
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token
from flask_restful import Resource

bcrypt = Bcrypt()

class RegisterAPI(Resource):
    def post(self):
        from app import mongo
        data = request.json
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")

        # Check input
        if not username or not email or not password:
            return {"message": "Mohon isi semua data"}, 400

        # Validasi jika username/email sudah terdaftar
        if mongo.db.users.find_one({"username": username}):
            return {"message": "Username sudah digunakan, mohon gunakan username lain!"}, 400

        # Hash password sebelum disimpan
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # Simpan user ke database
        user_id = mongo.db.users.insert_one({
            "username": username,
            "email": email,
            "password": hashed_password,
        }).inserted_id

        return {"message": "Register berhasil", "id": str(user_id)}, 200

class LoginAPI(Resource):
    def post(self):
        from app import mongo
        data = request.json
        username = data.get("username")
        password = data.get("password")

        # check input
        if not (username and password):
            return {"message": "Mohon isi semua data!"}, 400

        # get user data
        user = mongo.db.users.find_one({"username": username})
        # user dan password valid
        if not user or not bcrypt.check_password_hash(user["password"], password):
            return {"message": "Username atau password salah!"}, 401
        
        # Generate JWT token
        access_token = create_access_token(identity=str(user["_id"]))
        return {"message": "Login successful", "access_token": access_token}, 200