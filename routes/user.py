from flask import jsonify, request, Blueprint
from pymongo import MongoClient
import json
from ..util.database import mydb

from ..util.jwt_verification import verify_admin, verify_user

user = Blueprint('user', __name__)


@user.route('/user/delete', methods=['GET'])
def deleteUser():
    data = request.json
    print("delete route... ")
    if not data:
        return jsonify({
            'status': 0,
            'message': 'missing form data'
        })

    email = data['email']
    
    access_token = request.headers['ACCESS_TOKEN']

    verification = verify_admin(access_token=access_token)
   
    # veri_data= json.loads(verification.get_json())
    if verification[0]['status'] == 0:
        return jsonify({
            'status':0,
            'message':'user verfication failed'
        })
  
    if 'users' not in mydb.list_collection_names():
        mydb.create_collection('users')
   
    user = mydb.users.find_one({'email': email})
    
    if user is None:
        return jsonify({
            "status": 0,
            "message": "user not found with given email"
        })
    else:
        mydb.users.delete_one({'email': email})
        return jsonify({
            "status": 1,
            "message": "User deleted successfully."
        })
     


@user.route('/user/add', methods=['POST'])
def addUser():
    data = request.json
    if not data:
        return jsonify({
            'status': 0,
            'message': 'missing form data'
        })

    name = data['name']
    email = data['email']
    password = data['password']
    phone = data['phone']
    
    # print("data till this point ",data)

    access_token = request.headers['ACCESS_TOKEN']

    # print("access_token : ",access_token)
    verification = verify_admin(access_token=access_token)
    # print("verification : ", verification)
    # veri_data= json.loads(verification.get_json())
    if verification[0]['status'] == 0:
        return jsonify({
            'status':0,
            'message':'user verfication failed'
        })

    if 'users' not in mydb.list_collection_names():
        mydb.create_collection('users')

    user_data ={
        "name":str(name),
        "email":str(email),
        "password":str(password),
        "phone":str(phone)
    }
    user_id = mydb.users.insert_one(user_data)

    if user_id:
        return jsonify({
            'status': 1,
            'message': 'user added successfully',
            'userId': str(user_id)
        })
    return jsonify({
        'status': 0,
        'message': 'user addition failed'
    })


@user.route('/users', methods=['GET'])
def get_all_users():
    
    access_token = request.headers['ACCESS_TOKEN']

    # print("access_token : ",access_token)
    verification = verify_admin(access_token=access_token)
    # print("verification : ", verification)
    # veri_data= json.loads(verification.get_json())
    if verification[0]['status'] == 0:
        return jsonify({
            'status':0,
            'message':'user verfication failed'
        })
    
    # print("users verification ", verification)
    try:
        # print("created users ")
        if 'users' not in mydb.list_collection_names():
            mydb.create_collection('users')

        # print("created users ")
        users = []
        cnt=1
        users_data = mydb.users.find({})
        for user in users_data:
            # print('users -> ',user)
            users.append({
                'id':cnt,
                'name': user['name'],
                'email': user['email'],
                'phone': user['phone'],
                'access':'manager'
                # add other fields you want to retrieve from the user document
            })
            cnt=cnt+1
        # print("users ", users)
        return jsonify({
            'status':1,
            'data':users,
            'message':'successfully fetched all users'
        })
    except Exception as e:
        return jsonify({
            'status':0,
            'message':'database error'
        })

    
    
