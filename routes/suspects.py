from bson import Binary
from flask import jsonify, request, Blueprint
from ..util.database import mydb
from schema import suspect_schema
from ..util.jwt_verification import jwt_verification
import os

suspects = Blueprint('suspects', __name__)


@suspects.route('/suspects', methods=['GET'])
def get_suspects():
    access_token = request.headers['ACCESS_TOKEN']
    # print("Access token ", access_token)
    verification = jwt_verification(access_token=access_token)

    if verification['status'] != 201:
        return jsonify(verification)

    if 'suspects' not in mydb.list_collection_names():
        mydb.create_collection('suspects')
    data = mydb.suspects.find({})
    data1 = []
    for d in data:
        data1.append(d)

    print("data  =  ", data1, type(data1))
    return jsonify({"status": 0, "data": data1})


@suspects.route('/suspects/<string:id>', methods=['GET'])
def get_suspect(id):
    access_token = request.headers['ACCESS_TOKEN']
    verification = jwt_verification(access_token=access_token)

    if verification['status'] != 201:
        return jsonify(verification)

    if 'suspects' not in mydb.list_collection_names():
        mydb.create_collection('suspects')
    data = mydb['suspects'].find({'username': id})
    data1 = []
    for d in data:
        data1.append(d)
    return jsonify({"status": 0, "data": data1})


@suspects.route('/add/suspect', methods=['POST'])
def create_suspect():
    name = request.json['name']
    age = request.json['age']
    gender = request.json['gender']
    info = request.json['info'][0]
    location = info['location']
    time = info['time']
    image = request.json['image']
    remark = info['remark']
    access_token = request.headers['ACCESS_TOKEN']

    verification = jwt_verification(access_token=access_token)
    print("verification : ", verification)
    # veri_data= json.loads(verification.get_json())
    if verification['status'] != 201:
        return jsonify(verification)

    if 'suspects' not in mydb.list_collection_names():
        mydb.create_collection('suspects')
    data = {
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
        if key not in data and key == image:
            return jsonify({
                'status': 401,
                'message': 'Empty suspect image'
            })

    suspect_id = mydb.suspects.insert_one(data)
    if suspect_id:
        return jsonify({
            'status': 200,
            'message': 'suspect added successfully',
            'suspectId': suspect_id
        })
    return jsonify({
        'status': 401,
        'message': 'suspect addition failed'
    })
