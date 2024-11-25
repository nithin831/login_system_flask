from os import environ

class Config:
    SECRET_KEY = "nithin"  # or load from environment
    DATABASE_URL = environ.get('DB_URL')
