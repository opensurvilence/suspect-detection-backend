from pymongo import MongoClient
import os
import jwt
from .database import mydb


def jwt_verification(access_token):
    try:
        data = jwt.decode(access_token, os.getenv('JWT_SECRET_KEY'), algorithms=["HS256"])

        if mydb.users.find_one({'username': data['sub']}):
            return {
                'status': 201,
                'message': 'user found',
                'username': data['sub']
            }
        else:
            return {
                'status': 401,
                'message': 'You are not authorised to perform this action...kindly Login again'
            }
    except Exception as e:

        return {
            'status': 401,
            'message': 'Session Expired...Login again'
        }
