from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from datetime import datetime
from werkzeug.security import generate_password_hash


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vehicle_parking.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String,unique=True,nullable=False)
    email = db.Column(db.String,nullable=False)
    password = db.Column(db.String,nullable=False)
    role = db.Column(db.String,default='user')

class Category(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String,unique=True,nullable=False)

with app.app_context():
    db.create_all()

    if User.query.filter_by(username='admin').first() is None:
    
        admin_password = generate_password_hash('admin123')
        admin = User(username='admin',email=
                'admin@grocery.com',password=admin_password,role='admin')
        db.session.add(admin)
        db.session.commit()
    else:
        print("admin already exists")
