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

    # GitHub OAuth configuration
    GITHUB_CLIENT_ID = environ.get("GITHUB_CLIENT_ID")
    GITHUB_CLIENT_SECRET = environ.get("GITHUB_CLIENT_SECRET")
    GITHUB_AUTH_URL = environ.get("GITHUB_AUTH_URL")
    GITHUB_TOKEN_URL = environ.get("GITHUB_TOKEN_URL")
    GITHUB_API_URL = environ.get("GITHUB_API_URL")

    # google OAuth config
    GOOGLE_CLIENT_ID=environ.get("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET=environ.get("GOOGLE_CLIENT_SECRET")
    GOOGLE_AUTH_URL=environ.get("GOOGLE_AUTH_URL")
    GOOGLE_TOKEN_URL=environ.get("GOOGLE_TOKEN_URL")
    GOOGLE_API_URL=environ.get("GOOGLE_API_URL")
    GOOGLE_REDIRECT_URL=environ.get("GOOGLE_REDIRECT_URL")

    LINKEDIN_CLIENT_ID = environ.get("LINKEDIN_CLIENT_ID")
    LINKEDIN_CLIENT_SECRET = environ.get("LINKEDIN_CLIENT_SECRET")
    LINKEDIN_AUTH_URL = environ.get("LINKEDIN_AUTH_URL")
    LINKEDIN_TOKEN_URL = environ.get("LINKEDIN_TOKEN_URL")
    LINKEDIN_API_URL = environ.get("LINKEDIN_API_URL")
    LINKEDIN_REDIRECT_URL = environ.get("LINKEDIN_REDIRECT_URL")

    # Facebook OAuth configuration
    FACEBOOK_CLIENT_ID = environ.get("FACEBOOK_CLIENT_ID")
    FACEBOOK_CLIENT_SECRET = environ.get("FACEBOOK_CLIENT_SECRET")
    FACEBOOK_AUTH_URL = environ.get("FACEBOOK_AUTH_URL")
    FACEBOOK_TOKEN_URL = environ.get("FACEBOOK_TOKEN_URL")
    FACEBOOK_API_URL = environ.get("FACEBOOK_API_URL")

    # Frontend URL (local host)
    FRONTEND_URL = environ.get("FRONTEND_URL")

# For email
from flask_mail import Mail
mail = Mail()