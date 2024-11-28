import os

class Config:
    # MONGO DB URI
    MONGO_URI = "mongodb://localhost:27017/myDatabase"
    # Secret key for JWT
    SECRET_KEY = os.getenv("SECRET_KEY")