from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash
import secrets
from secrets import token_hex
from flask import Flask
from flask_login import UserMixin
from flask_login import LoginManager


db = SQLAlchemy()
login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
  
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    token = db.Column(db.String(32), index=True, unique=True)

    def __init__(self, first_name, last_name, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = generate_password_hash(password)
        self.token = token_hex(16)


    def __repr__(self):
        return f"<User {self.email}>"

    def generate_password_hash(self, password):
        self.password = generate_password_hash(password)
    


class Meme(db.Model):
    __tablename__ = 'memes'
    meme_id = db.Column(db.Integer, primary_key=True)
    meme_name = db.Column(db.String(50), nullable=False)
    img_id = db.Column(db.Integer, db.ForeignKey('images.id'), nullable=False)
    meme_caption = db.Column(db.String(50), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    

    def __init__(self, meme_name, img_id, meme_caption):
        self.meme_name = meme_name
        self.img_id = img_id
        self.meme_caption = meme_caption
    
    def serialize(self):
        return {
            'meme_id': self.meme_id,
            'meme_name': self.meme_name,
            'img_id': self.img_id,
            'meme_caption': self.meme_caption,
            'date_created': self.date_created,
            
        }
      

    def __repr__(self):
        return f"<Meme {self.meme_name}>"
    


class Image(db.Model):
    __tablename__ = 'images'
    id = db.Column(db.Integer, primary_key=True)
    img_url = db.Column(db.String(50), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    

    def __init__(self, img_url):
        self.img_url = img_url
      
    def serialize(self):
        return {
            'id': self.id,
            'img_url': self.img_url,
            'date_created': self.date_created
        }

    def __repr__(self):
        return f"<Image {self.img_url}>"
    

