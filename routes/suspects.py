from bson import Binary
from flask import jsonify, request, Blueprint, send_file
from ..util.database import mydb
from ..schema import suspect_schema
from ..util.jwt_verification import verify_user,verify_admin
import os
import requests
import cv2
suspects = Blueprint('suspects', __name__)

import face_recognition
import base64
import io

from ..model.model import findSuspects
from .data import DUMMY_EMBEDDINGS

@suspects.route('/detect_faces', methods=['POST'])
def detect_faces():
    if not request.data:
        pass

    # image_data = request.data

    # if not image_data:
    #     pass
    blob = request.data

    # Decode the blob object
    data = base64.b64encode(blob)

    # Write the decoded data to a file
    with open('image.png', 'wb') as f:
        f.write(blob)
    
    # encoded_image = base64.b64decode(image_data)
    # print(type(encoded_image))


    result = findSuspects(data,DUMMY_EMBEDDINGS)

    mod_img=base64.b64decode(result['modified_img'])

    with open('res_image.png', 'wb') as f:
        f.write(blob)

    print("matched ids ",result['found_suspects'])
    print("detection complete")

    
    
    # # print('file name  =',fname)
    # fname='temp.jpeg'
    # if image_data:
    #     print(fname)
    #     # decoded_data = base64.b64decode(image_data)

    # create a file-like object from the decoded data
        # file = io.BytesIO(image_data)

    # # save the file to disk
        # with open('image.png', 'wb') as f:
            # f.write(file.read())
        # f.save(fname)
        # image_data=cv2.imread(fname)
    # Decode the base64 encoded string
    
    # Decode the image data from base64
    # image_bytes = base64.b64decode(encoded_image)
    
    # # Load the image using the face-recognition library
    # image = face_recognition.load_image_file(image_bytes)
    
    # # Detect the faces in the image using the face-recognition library
    # face_locations = face_recognition.face_locations(image)
    
    # # Draw boxes around the detected faces
    # for top, right, bottom, left in face_locations:
    #     cv2.rectangle(image, (left, top), (right, bottom), (0, 0, 255), 2)

    # # Encode the image back to base64 to send it back to the client
    # _, img_encoded = cv2.imencode('.jpg', image)
    # image_data = base64.b64encode(img_encoded).decode('utf-8')

    return jsonify({"message":"hello"})
@suspects.route('/image')
def get_image():
    filename = 'result_image.png'
    return send_file(filename, mimetype='image/png')

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
@suspects.route('/api/img', methods=['POST'])
def suspect_detection():
    video_file = request.files['video']
    video_file.save('video.mp4')
    

    cap = cv2.VideoCapture('video.mp4')
    while True:
        # Read a frame from the video
        ret, frame = cap.read()

       
        if frame:
        # Show the resulting frame
            cv2.imshow('frame', frame)

        # Exit if the 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Release the video capture object and destroy all windows
    cap.release()
    cv2.destroyAllWindows()
    return 'Video uploaded successfully!'


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
