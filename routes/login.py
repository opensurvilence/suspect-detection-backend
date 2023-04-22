import json

from flask import jsonify, request, Blueprint
from pymongo import MongoClient
from flask_jwt_extended import create_access_token
from ..util.database import mydb
import os

login = Blueprint('login', __name__)


@login.route('/login', methods=['POST'])
def auth_login():
    print('username ')

    if 'users' not in mydb.list_collection_names():
        mydb.create_collection('users')

    mycol = mydb["users"]
    try:
        username = request.json['username']
        password = request.json['password']
        if mycol.find_one({'username': username, 'password': password}):
            access_token = create_access_token(identity=username)
            return jsonify({'status': 200, 'message': 'OK', 'access_token': access_token})
        else:
            return jsonify({'status': 401, 'message': 'Login failed'})
    except Exception as e:
        return jsonify({
            'status': 501,
            'message': 'internal server'
        })
