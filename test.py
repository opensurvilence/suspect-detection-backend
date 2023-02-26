import os

import base64

with open("emp2.jpg", "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    img = open('image.txt',"w") 
    img.write(encoded_string)

    