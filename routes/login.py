import json

from flask import jsonify, request, Blueprint
from flask_jwt_extended import create_access_token
from ..util.database import mydb


login = Blueprint('login', __name__)


@login.route('/login', methods=['POST'])
def auth_login():
    print('username ')

    if 'users' not in mydb.list_collection_names():
        mydb.create_collection('users')

    mycol = mydb["users"]
    try:
        data = request.json
        if not data:
            return {
                "status":0,
                "message":"data missing"
            },404
        username = data['username']
        password = data['password']
        
        if mycol.find_one({'username': username, 'password': password}):
            access_token = create_access_token(identity=username)

            return {
                'status': 1, 
                'message': 'user found with given credentials', 
                'access_token': access_token
                },200
        else:
            return {
                'status': 0,
                'message': 'Login failed'
                },401
    except Exception as e:
        return {
            'status': 0,
            'message': 'internal server error'
        },404
