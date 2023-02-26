from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from bson.binary import Binary
import os
import jwt
import json
from schema import suspect_schema
app = Flask(__name__)
app.config['PORT'] = 5001
app.config['DEBUG'] = True
CORS(app)
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
JWT = JWTManager(app)

client = MongoClient(
    f"mongodb+srv://{os.getenv('DB_USERNAME')}:{os.getenv('DB_PASSWORD')}@cluster0.acrcjxy.mongodb.net/?retryWrites=true&w=majority")
mydb = client['miniproject']


def jwt_verification(access_token):
    try:
        data = jwt.decode(access_token, os.getenv('JWT_SECRET_KEY'),algorithms=["HS256"])
     
        if mydb.users.find_one({'username': data['sub']}):
            return {
                'status': 201,
                'message': 'user found',
                'username':data['sub']
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


@app.route('/login', methods=['POST'])
def authlogin():
    print('username ')
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
            'status':501,
            'message':'internal server'
        })

@app.route('/add/suspect', methods=['POST'])
def createSuspect():
    name = request.json['name']
    age = request.json['age']
    gender = request.json['gender']
    info=request.json['info'][0]
    location = info['location']
    time = info['time']
    image = request.json['image']
    remark = info['remark']
    access_token = request.headers['ACCESS_TOKEN']

    verification = jwt_verification(access_token=access_token)
    print("verification : ",verification)
    # veri_data= json.loads(verification.get_json())
    if verification['status'] != 201:
        return jsonify(verification)
    
    if 'suspects' not in mydb.list_collection_names():
        mydb.create_collection('suspects')
    data = {
        'name': name,
        'age': age,
        'username':verification['username'],
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

@app.route('/suspects', methods=['GET'])
def getSuspects():
    access_token = request.headers['ACCESS_TOKEN']
    verification = jwt_verification(access_token=access_token)

    if verification['status'] != 201:
        return jsonify(verification)

    if 'suspects' not in mydb.list_collection_names():
        mydb.create_collection('suspects')
    data = mydb['suspects']
    return jsonify({"status": 0,"data":data})
    
@app.route('/suspects/<string:id>', methods=['GET'])
def getSuspect():
    access_token = request.headers['ACCESS_TOKEN']
    verification = jwt_verification(access_token=access_token)

    if verification['status'] != 201:
        return jsonify(verification)

    if 'suspects' not in mydb.list_collection_names():
        mydb.create_collection('suspects')
    data = mydb['suspects'].find({'username':id})
    return jsonify({"status":0, "data":data})


if __name__ == '__main__':
    print("running...")
    app.run(debug=True, port=5001)
