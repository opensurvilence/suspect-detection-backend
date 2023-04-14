from flask import  jsonify, request, Blueprint
from pymongo import MongoClient
from ..Utilities.jwt_verification import jwt_verification
import os


suspects = Blueprint('suspects', __name__)

client = MongoClient(
    f"mongodb+srv://{os.getenv('DB_USERNAME')}:{os.getenv('DB_PASSWORD')}@cluster0.acrcjxy.mongodb.net/?retryWrites=true&w=majority")
mydb = client['miniproject']


@suspects.route('/suspects', methods=['GET'])
def getSuspects():
    access_token = request.headers['ACCESS_TOKEN']
    # print("Access token ", access_token)
    verification = jwt_verification(access_token=access_token)

    if verification['status'] != 201:
        return jsonify(verification)    

    if 'suspects' not in mydb.list_collection_names():
        mydb.create_collection('suspects')
    data = mydb.suspects.find({})
    data1=[]
    for d in data:
        data1.append(d)

    print("data  =  " ,data1 , type(data1))
    return jsonify({"status": 0,"data":data1})
    
@suspects.route('/suspects/<string:id>', methods=['GET'])
def getSuspect(id):
    access_token = request.headers['ACCESS_TOKEN']
    verification = jwt_verification(access_token=access_token)

    if verification['status'] != 201:
        return jsonify(verification)

    if 'suspects' not in mydb.list_collection_names():
        mydb.create_collection('suspects')
    data = mydb['suspects'].find({'username':id})
    data1=[]
    for d in data:
        data1.append(d)
    return jsonify({"status":0, "data":data1})
