from flask import Flask
from flask_restful import Api
from config import Config
from flask_pymongo import PyMongo
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

# initialize Flask-RESTful API
api = Api(app)

# initialize database
mongo = PyMongo(app)

from routes import initialize_routes
initialize_routes(api)


if __name__ == "__main__":
    app.run(debug=True)