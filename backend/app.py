from flask_sqlalchemy import SQLAlchemy
from flask import Flask,jsonify,make_response, request
from flask_restful import Api,Resource, reqparse
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, unset_jwt_cookies
from flask_cors import CORS
from model import db,User,Category
from werkzeug.security import check_password_hash,generate_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vehicle_parking.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'vehicle'

db.init_app(app)
CORS(app,origins="*")

jwt = JWTManager(app)
api = Api(app)


@app.route('/',methods=['GET'])
def home():
    return jsonify({"message":"Welcome to the Vehicle Parking System API"}), 200

@app.route('/signup',methods=['POST'])
def signup():
        email = request.json.get('email')
        username = request.json.get('username')
        password = request.json.get('password')
        role = request.json.get('role','user')

        username_exists = User.query.filter_by(username=username).first()

        if username_exists:
            return jsonify({"message":"Username already exists"}), 400
        else:
            user_password = generate_password_hash(password)
            new_user = User(email=email,username=username,password=user_password,role=role)

            db.session.add(new_user)
            db.session.commit()
            return jsonify({"message":"User created successfully"}), 201
    
@app.route('/login',methods=['POST'])
def login():
        username = request.json.get('username')
        password = request.json.get('password')

        user = User.query.filter_by(username=username).first()

        if not user or check_password_hash(user.password,password) is False:
            return jsonify({"message":"Invalid username or password"}), 401
        else:
            access_token = create_access_token(identity={"username":user.username,"role":user.role})
            user_info = {
                 "username":user.username,
                 "role":user.role,
                 "email":user.email
            }
            return jsonify({"access_token":access_token,"user_info":user_info}), 200
        
@app.route('/logout',methods=['POST'])
@jwt_required()
def logout():
     role = get_jwt_identity()
     print(role)
     resp = {"message":"Logout successful"}
     unset_jwt_cookies((jsonify(resp)))
     return resp,200


@app.route('/user_info',methods=['GET'])
@jwt_required()
def user_info():
     users = User.query.all()
     user_info = [
          {
               "id":user.id,
               "username":user.username,
               "role"   :user.role,

          } for user in users
     ]

     return user_info,200


if __name__ == '__main__':
    app.run(debug=True)