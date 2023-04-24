import os
import jwt
from .database import mydb


def verify_user(access_token):
    try:
        data = jwt.decode(access_token, os.getenv('JWT_SECRET_KEY'), algorithms=["HS256"])

        if mydb.users.find_one({'username': data['sub']}):
            return {
                'status': 1,
                'message': 'user found',
                'username': data['sub']
            },201
        else:
            return {
                'status': 0,
                'message': 'unauthorized user'
            },404
    except Exception as e:

        return {
            'status': 0,
            'message': 'Session Expired'
        },404

def verify_admin(access_token):
    try:
        data = jwt.decode(access_token, os.getenv('JWT_SECRET_KEY'), algorithms=["HS256"])
        # print("admin data " , data)
        if mydb.super_admins.find_one({'username': data['sub']}):
            return {
                'status': 1,
                'message': 'user found',
                'username': data['sub']
            },201
        else:
            return {
                'status': 0,
                'message': 'unauthorized user'
            },404
    except Exception as e:

        return {
            'status': 0,
            'message': 'Session Expired'
        },404
