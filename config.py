# config.py
import os

class Config:
    SECRET_KEY = os.urandom(24)  # Random secret key
    SQLALCHEMY_DATABASE_URI = 'sqlite:///C:/Users/hussa/password-manager/passwords.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable modification tracking for performance
