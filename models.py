from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin  # Import UserMixin from flask_login

db = SQLAlchemy()

# User Model
class User(db.Model, UserMixin):  # Inherit from UserMixin
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)  # Stored hashed password

    passwords = db.relationship('Password', backref='owner', lazy=True)
    
    # Add is_active property for Flask-Login
    is_active_flag = db.Column(db.Boolean, default=True, nullable=False)

    # Property for is_active (Flask-Login expects it)
    @property
    def is_active(self):
        return self.is_active_flag

# Password Model
class Password(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False)
    password = db.Column(db.String(255), nullable=False)  # Encrypted password
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
