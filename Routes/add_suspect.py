from flask import  jsonify, request, Blueprint

from pymongo import MongoClient
from bson.binary import Binary
import os
from ..Utilities.jwt_verification import jwt_verification
from ..schema import suspect_schema 

client = MongoClient(
    f"mongodb+srv://{os.getenv('DB_USERNAME')}:{os.getenv('DB_PASSWORD')}@cluster0.acrcjxy.mongodb.net/?retryWrites=true&w=majority")
mydb = client['miniproject']


add_suspect = Blueprint('add_suspect', __name__)


@add_suspect.route('/add/suspect', methods=['POST'])
def createSuspect():
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
