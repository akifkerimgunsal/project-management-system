import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql://postgres:akg@localhost:5432/todolist_deneme')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'default_secret_key')
    DEBUG = os.environ.get('DEBUG', True)
    HOST = os.environ.get('HOST', '127.0.0.1')
