# import os

from os import environ

class Config:
    # SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "postgresql://postgres:nithin@localhost:5432/product")
    SQLALCHEMY_DATABASE_URI = environ.get('DB_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
