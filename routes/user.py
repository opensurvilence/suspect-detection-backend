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
            'status': 1,
            'message': 'missing form data'
        }, 404

    email = data['email']

    access_token = request.headers['ACCESS_TOKEN']

    verification = jwt_verification(access_token=access_token)
    print("verification : ", verification)
    # veri_data= json.loads(verification.get_json())
    if verification['status'] != 201:
        return jsonify(verification)

    if 'users' not in mydb.list_collection_names():
        mydb.create_collection('users')

    user = mydb.users.find_one({'email': email})
    if user is None:
        return jsonify({
            "status": 404,
            "message": "User does not exist."
        })
    else:
        mydb.users.delete_one({'email': email})
        return jsonify({
            "status": 200,
            "message": "User deleted successfully."
        })


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
    if verification['status'] != 201:
        return jsonify(verification)

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
        return jsonify({
            'status': 200,
            'message': 'user added successfully',
            'userId': user_id
        })
    return jsonify({
        'status': 401,
        'message': 'user addition failed'
    })
