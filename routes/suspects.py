from bson import Binary
from flask import jsonify, request, Blueprint
from ..util.database import mydb
from ..schema import suspect_schema
from ..util.jwt_verification import verify_user,verify_admin
import os

suspects = Blueprint('suspects', __name__)


@suspects.route('/suspects', methods=['GET'])
def get_suspects():
    access_token = request.headers['ACCESS_TOKEN']
    # print("Access token ", access_token)
    verification = verify_user(access_token=access_token)

    if verification[0]['status'] == 0:
        return jsonify({
            'status': 0,
            'message': 'invalid token or session expired'
        })

    if 'suspects' not in mydb.list_collection_names():
        mydb.create_collection('suspects')
    data = mydb.suspects.find({})
    data1 = []
    for d in data:
        data1.append(d)

    # print("data  =  ", data1, type(data1))
    return jsonify({
        "status": 1,
        "data": data1
    })


@suspects.route('/suspects/<string:id>', methods=['GET'])
def get_suspect(id):
    access_token = request.headers['ACCESS_TOKEN']
    verification = verify_user(access_token=access_token)

    if verification[0]['status'] == 0:
        return jsonify({
        "status": 0,
        "message": "user verfication failed"
    })

    if 'suspects' not in mydb.list_collection_names():
        mydb.create_collection('suspects')
    data = mydb['suspects'].find({'username': id})
    data1 = []
    for d in data:
        data1.append(d)
    return jsonify({
        "status": 1,
        "data": data1
    })


@suspects.route('/add/suspect', methods=['POST'])
def create_suspect():
    data = request.json
    if not data:
        return jsonify({
            'status': 0,
            'message': 'missing request',
        })

    name = data['name']
    age = data['age']
    gender = data['gender']
    info = data['info'][0]
    location = info['location']
    time = info['time']
    image = data['image']
    remark = info['remark']
    access_token = request.headers['ACCESS_TOKEN']

    verification = verify_user(access_token=access_token)
    # print("verification : ", verification)
    # veri_data= json.loads(verification.get_json())
    if verification['status'] == 0:
        return jsonify({
            'status':0,
            'message':'user verification failed'
        })

    if 'suspects' not in mydb.list_collection_names():
        mydb.create_collection('suspects')
    user_data = {
        'name': name,
        'age': age,
        'username': verification['username'],
        'gender': gender,
        'image': Binary(image),
        'info': [
            {
                'location': location,
                'time': time,
                'remark': remark
            }
        ]

    }
    for key, value in suspect_schema.items():
        if key not in user_data and key == image:
            return jsonify({
                'status': 0,
                'message': 'missing suspect image'
            })

    suspect_id = mydb.suspects.insert_one(data)
    if suspect_id:
        return jsonify({
            'status': 1,
            'message': 'suspect added successfully',
            'suspectId': suspect_id
        })
    return jsonify({
        'status': 0,
        'message': 'suspect addition failed'
    })
