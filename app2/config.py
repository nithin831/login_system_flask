from os import environ

class Config:
    SECRET_KEY = environ.get("SECRET_KEY")  # for jwt
    DATABASE_URL = environ.get('DB_URL')
    JWT_EXPIRATION_SECONDS = 3600
    # REDIS_HOST = "redis"
    # REDIS_PORT = 6379
    
    # Email Configuration
    MAIL_SERVER = environ.get("MAIL_SERVER")
    MAIL_PORT =  environ.get("MAIL_PORT")
    MAIL_USE_TLS = environ.get("MAIL_USE_TLS")
    MAIL_USERNAME = environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = environ.get("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = environ.get("MAIL_DEFAULT_SENDER")

    # Frontend URL (for email verification link)
    FRONTEND_URL = "http://localhost:4000"

# For email
from flask_mail import Mail
mail = Mail()