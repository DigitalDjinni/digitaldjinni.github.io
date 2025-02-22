from app import db  
from flask_login import UserMixin

# User model for storing user data in the database.
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, default=False) # Setting the default to user. Role is changed inside the database

# Trip model for storing trip data in the database
class Trip(db.Model):
    __tablename__ = 'trips'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    length = db.Column(db.String(50))
    start = db.Column(db.Date)
    resort = db.Column(db.String(100))
    per_person = db.Column(db.Float)
    image = db.Column(db.String(100))
    description = db.Column(db.Text)
