import json
import os
from pymongo import MongoClient
from flask import jsonify, request, Blueprint
from flask_jwt_extended import create_access_token
# from ..util.database import mydb

client = MongoClient(
    f"mongodb+srv://{os.getenv('DB_USERNAME')}:{os.getenv('DB_PASSWORD')}@cluster0.acrcjxy.mongodb.net/?retryWrites=true&w=majority")

mydb = client['miniproject']

login = Blueprint('login', __name__)


@login.route('/login', methods=['POST'])
def auth_login():

    if 'users' not in mydb.list_collection_names():
        mydb.create_collection('users')

    mycol = mydb["users"]
    try:
        data = request.json
        if not data:
            return jsonify({
                "status":0,
                "message":"data missing"
            })
        username = data['username']
        password = data['password']
        
        if mycol.find_one({'username': username, 'password': password}):
            access_token = create_access_token(identity=username)

            return jsonify({
                'status': 1, 
                'message': 'user found with given credentials', 
                'access_token': access_token
                })
        else:
            return jsonify({
                'status': 0,
                'message': 'Login failed'
                })
    except Exception as e:
        jsonify({
            'status': 0,
            'message': 'internal server error'
        })



@login.route('/login/admin', methods=['POST'])
def auth_login_admin():
   

    if 'super_admins' not in mydb.list_collection_names():
        mydb.create_collection('super_admins')

    mycol = mydb["super_admins"]
    try:
        data = request.json
        if not data:
            return jsonify({
                "status":0,
                "message":"data missing"
            })
        username = data['username']
        password = data['password']
        
        if mycol.find_one({'username': username, 'password': password}):
            access_token = create_access_token(identity=username)

            return jsonify({
                'status': 1, 
                'message': 'user found with given credentials', 
                'access_token': access_token
                })
        else:
            return jsonify({
                'status': 0,
                'message': 'Login failed'
                })
    except Exception as e:
        return jsonify({
            'status': 0,
            'message': 'internal server error'
        })
