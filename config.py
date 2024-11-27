import os

class Config:
    # DEBUG = True
    MONGO_URI = "mongodb://localhost:27017/myDatabase"
    SECRET_KEY = os.getenv("SECRET_KEY")