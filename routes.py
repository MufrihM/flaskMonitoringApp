from flask import request, jsonify
from flask_restful import Resource
from models import product_serializer, user_serializer, serialize_list, order_serializer, order_details_serializer, temperature_serializer, humidity_serializer
from flask_pymongo import ObjectId
from flask_jwt_extended import jwt_required, get_jwt_identity
from auth import RegisterAPI, LoginAPI

class ProductListAPI(Resource):
    @jwt_required()
    def get(self):
        # mengambil semua produk
        from app import mongo
        products = mongo.db.products.find()
        return jsonify(serialize_list(products, product_serializer))
    
    def post(self):
        # membuat produk baru
        from app import mongo
        data = request.json
        product_id = mongo.db.products.insert_one({
            "name": data.get("name"),
            "price": data.get("price")
        }).inserted_id
        return jsonify(product_serializer(mongo.db.products.find_one({"_id": product_id})))
    
class ProductAPI(Resource):
    @jwt_required()
    def get(self, product_id):
        # mengambil detail produk berdasarkan id
        from app import mongo
        product = mongo.db.products.find_one({"_id": ObjectId(product_id)})
        if product:
            return jsonify(product_serializer(product))
        return jsonify({"message": "Product not found"}), 404
    
    def put(self, product_id):
        # memperbarui produk berdasarkan id
        from app import mongo
        data = request.json
        updated_product = mongo.db.products.find_one_and_update(
            {"_id": ObjectId(product_id)},
            {"$set": {"name": data.get("name"), "price": data.get("price")}},
            return_document=True
        )
        if updated_product:
            return jsonify(product_serializer(updated_product))
        return jsonify({"message": "Product not found"}), 404
    
    def delete(self, product_id):
        # Menghapu produk berdasarkan id
        from app import mongo
        result = mongo.db.products.delete_one({"_id": ObjectId(product_id)})
        if result.deleted_count:
            return jsonify({"message": "Product deleted successfully"})
        return jsonify({"message": "Product not found"}), 404
    
class UserListAPI(Resource):
    @jwt_required()
    def get(self):
        # mengambil data user
        from app import mongo
        users = mongo.db.users.find()
        return jsonify(serialize_list(users, user_serializer))
    
class OrderAPI(Resource):
    @jwt_required()
    def post(self):
        from app import mongo
        data = request.json
        user_id = get_jwt_identity() # get user ID using JWT Token
        product_ids = data.get("product_ids")

        # vallidasi user
        user = mongo.db.users.find_one({"id": ObjectId(user_id)})
        if not user:
            return jsonify({"message": "User not found"}), 404
        
        # validasi data product
        products = []
        total_amount = 0
        for product_id in product_ids:
            product = mongo.db.products.find_one({"id": ObjectId(product_id)})
            if not product:
                return jsonify({"message": f"Product with id {product_id} not found"}), 404
            products.append(product)
            total_amount += product["price"]

        # data dikirim ke mongodb
        order_id = mongo.db.orders.insert_one({
            "user_id": ObjectId(user_id),
            "product_ids": [ObjectId(product_id) for product_id in product_ids],
            "total_amount": total_amount,
            "status": data.get("status", "pending")
        }).inserted_id
        return jsonify({"id": str(order_id), "message": "Order created successfully"})
    
    def get(self, order_id):
        from app import mongo
        order = mongo.db.orders.find_one({"id": ObjectId(order_id)})
        if not order:
            return jsonify({"message": "Order not found"}), 404
        
        # ambil detail user
        user = mongo.db.users.find_one({"id": ObjectId(order['user_id'])})
        if not user:
            return jsonify({"message": "User not found"}), 404
        
        # ambil detail product
        products = []
        for product_id in order['product_ids']:
            product = mongo.db.products.find_one({"id": ObjectId(product_id)})
            if product:
                products.append(product)

        return jsonify(order_details_serializer(order, user, products))

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
    api.add_resource(ProductListAPI, '/')
    api.add_resource(ProductAPI, '/products/<product_id>')
    api.add_resource(UserListAPI, '/users')
    api.add_resource(TemperatureAPI, '/temp')
    api.add_resource(HumidityAPI, '/humid')

    #  Endpoint untuk autentikasi
    api.add_resource(RegisterAPI, '/register')
    api.add_resource(LoginAPI, '/login')