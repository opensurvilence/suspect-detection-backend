#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 23 15:59:54 2023

@author: avinash
"""

# !pip install deepface cmake dlib

from PIL import Image
from io import BytesIO
import base64
from deepface import DeepFace
import numpy as np
import matplotlib.pyplot as plt
import cv2

# img = numpy array(BGR) or base64 or img_path

def decodeImage(base64Img):
    img = base64.b64decode(base64Img)
    pil_image = Image.open(BytesIO(img))
    return np.array(pil_image)


def getRepresentations(img):
    if(isinstance(img, bytes)):
        img = decodeImage(img)

    obj = DeepFace.represent(
        img_path=img,
        model_name='Facenet',
        # detector_backend='dlib',
        detector_backend='ssd',
        enforce_detection=False,
    )
    return obj


def getSuspectEmbedding(img):
    obj = getRepresentations(img)
    return obj[0]['embedding']


# find match

THREESHOLD_VALUE = 0.5  # facenet

def encodeImg(img):
    # pil_img = Image.fromarray((img * 255).astype(np.uint8))
    # img_bytes = BytesIO()
    # pil_img.save(img_bytes, format='PNG')
    # img_bytes.seek(0)
    # base64_string = base64.b64encode(img_bytes.read())

    # # convert bytes to string
    # # base64_string = base64_string.decode('utf-8')

    # return base64_string
    retval, buffer = cv2.imencode('.jpeg', img)
    jpg_as_text = base64.b64encode(buffer)
    return jpg_as_text

def findCosineDistance(vector_1, vector_2):
    a = np.matmul(np.transpose(vector_1), vector_2)
    b = np.matmul(np.transpose(vector_1), vector_1)
    c = np.matmul(np.transpose(vector_2), vector_2)
    return 1 - (a / (np.sqrt(b) * np.sqrt(c)))

# suspects_embeddings = [{id, embedding}, ...]

def findSuspects(input_img, suspects_embeddings):
    input_representations = getRepresentations(input_img)
    # print("input image : ",input_representations)
    found_suspects = []  # ids of matched suspects
    matched_reps = []  # ids of matched faces in input
    i = 0

    for rep in input_representations:
        for suspect in suspects_embeddings:
            distance = findCosineDistance(
                suspect['embedding'], rep['embedding'])
            if distance < THREESHOLD_VALUE:
                found_suspects.append(suspect['id'])
                matched_reps.append(i)
        i = i+1

    # show bounding box around found suspects

    # if base64Img

    if(isinstance(input_img, bytes)):
        img = decodeImage(input_img)

    # if numpy array

    elif(isinstance(input_img, np.ndarray)):
        img = input_img

    # if path
    else:
        img = plt.imread(input_img)

    for id in matched_reps:
        facial_area = input_representations[id]['facial_area']
        x = facial_area['x']
        y = facial_area['y']
        w = facial_area['w']
        h = facial_area['h']
        img = cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 0), 2)
    
    plt.imshow(img)
    cv2.imwrite('result_image.png',img)
    base64_img = encodeImg(img)

    return {'found_suspects': found_suspects, 'modified_img': base64_img}




# testing
import os

root = os.getcwd()
sus_dir = os.path.join(root, 'model/suspects')


def dummy_embeddings(sus_dir):
    sus_embeddings = []
    i = 1
    for sus_img in os.listdir(sus_dir):
        e = getSuspectEmbedding(os.path.join(sus_dir, sus_img))
        sus_embeddings.append({'id': i, 'embedding': e})
        i += 1
    return sus_embeddings

# sus_embeddings = dummy_embeddings(sus_dir)
# print(sus_embeddings)

# for sus_img in os.listdir(sus_dir):
#     print(sus_img)

# input_img = '/home/avinash/Desktop/mini_project/test_img.jpeg'
# input_img = cv2.imread(input_img)
# results = findSuspects(input_img, sus_embeddings)

# plt.imshow(results['modified_img'])
# plt.show()

# results['found_suspects']

# ts = getRepresentations(input_img)
# len(ts)


# input_path = '/home/avinash/Desktop/mini_project/test_img.jpeg'

# with open(input_path, "rb") as image_file:
#     encoded_string = base64.b64encode(image_file.read())

# res = findSuspects(encoded_string, sus_embeddings)

# len(getRepresentations(encoded_string))


