import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev_secret_key')
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "postgresql://postgres:Max.40WSQL@localhost/maps")
    SQLALCHEMY_TRACK_MODIFICATIONS = False