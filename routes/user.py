from flask import jsonify, request, Blueprint
from pymongo import MongoClient
import os
from ..util.database import mydb

from util.jwt_verification import jwt_verification

user = Blueprint('user', __name__)


@user.route('/user/delete/id', methods=['GET'])
def deleteUser():
    data = request.json
    if not data:
        return {
            'status': 0,
            'message': 'missing form data'
        }, 404

    email = data['email']

    access_token = request.headers['ACCESS_TOKEN']

    verification = jwt_verification(access_token=access_token)
    print("verification : ", verification)
    # veri_data= json.loads(verification.get_json())
    if verification['status'] == 0:
        return {
            'status':0,
            'message':'user verfication failed'
        },403

    if 'users' not in mydb.list_collection_names():
        mydb.create_collection('users')

    user = mydb.users.find_one({'email': email})
    if user is None:
        return {
            "status": 0,
            "message": "user not found with given email"
        },404
    else:
        mydb.users.delete_one({'email': email})
        return {
            "status": 1,
            "message": "User deleted successfully."
        },200


@user.route('/user/add', methods=['POST'])
def addUser():
    data = request.json
    if not data:
        return jsonify({
            'status': 404,
            'message': 'missing form data'
        })

    name = data['name']
    email = data['email']
    password = data['password']
    phone = data['phone']

    access_token = request.headers['ACCESS_TOKEN']

    verification = jwt_verification(access_token=access_token)
    print("verification : ", verification)
    # veri_data= json.loads(verification.get_json())
    if verification['status'] == 0:
        return {
            'status':0,
            'message':'user verfication failed'
        },403

    if 'users' not in mydb.list_collection_names():
        mydb.create_collection('users')

    user_data = {
        'name': name,
        'email': email,
        'password': password,
        'phone': phone
    }

    user_id = mydb.users.insert_one(user_data)

    if user_id:
        return {
            'status': 1,
            'message': 'user added successfully',
            'userId': user_id
        },200
    return {
        'status': 0,
        'message': 'user addition failed'
    },400
