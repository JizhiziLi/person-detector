from flask import Flask, render_template, request
from person_detector import module_1, module_2
from .config import *
import os

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


#####
# route /upload is used to upload an image and store in
# static directory
# eg. curl -i -X POST -F image=@test.png "127.0.0.1:5000/upload"
#####

@app.route('/upload', methods=['POST'])
def upload_image():
    file = request.files['image']
    f = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(f)
    return 'SUCCESS'


#####
# route /process is used to process an image based on its name and
# module type (1 or 2)
# eg. curl -H "Content-Type: application/json" -X POST -d '{"imageName":"test.jpg","moduleType":1}' "127.0.0.1:5000/process"
#####
@app.route('/process', methods=['POST'])
def process_image():
    body = request.get_json()
    imageName = body[IMAGENAME]
    if body['moduleType'] == 1:
        module_1._processImage(imageName)
    elif body['moduleType'] == 2:
        module_2._processImage(imageName)
    else:
        # TODO: should format to error logging
        print('You should define imageName and moduleType in your JSON.')
    return 'SUCCESS'

#####
# route /validate is used to validate if an image is valid or not
# (contains people or not)
# eg. curl -H "Content-Type: application/json" -X POST -d '{"imageName":"test.jpg"}' "127.0.0.1:5000/validate"
#####
@app.route('/validate', methods=['POST'])
def validate_image():
    try:
        body = request.get_json()
        imageName = body[IMAGENAME]
        validate = module_1._validateImage(imageName)
        return str(validate)
    except:
        return IMAGE_NAME_ERROR
    


#####
# route /validate is used to process an image based on its name and
# module type (1 or 2)
# eg. curl -H "Content-Type: application/json" -X POST -d '{"imageName":"test.jpg"}' "127.0.0.1:5000/edge"
#####
@app.route('/edge', methods=['POST'])
def detect_edge():
    try:
        body = request.get_json()
        imageName = body[IMAGENAME]
        module_1._detectEdge(imageName)
        return 'Edge has been saved in folder /static/single_image/processed'
    except:
        return IMAGE_NAME_ERROR



#####
# route /validate_test is used to test validation method on batch of images
# path of test folder is defined in config.py
# eg. curl -H "Content-Type: application/json" -X POST  "127.0.0.1:5000/validate_test"
#####
@app.route('/validate_test', methods=['POST'])
def validate_image_test():
    try:
        validate = module_1._validateImageTest()
        return 'Please see results in folder /static/batch_images/validate_result'
    except:
        return IMAGE_NAME_ERROR


#####
# route /validate_test is used to test validation method on batch of images
# path of test folder is defined in config.py
# eg. curl -H "Content-Type: application/json" -X POST  "127.0.0.1:5000/validate_test"
#####
@app.route('/extract_frame', methods=['POST'])
def extract_frame():
    try:
        body = request.get_json()
        module_1._extractFrame(body)
        return 'Please see results in folder /static/batch_images/validate_result'
    except:
        return IMAGE_NAME_ERROR




#####
# route /extract_size is used to test validation method on batch of images
# path of test folder is defined in config.py
# eg. curl -H "Content-Type: application/json" -X POST  "127.0.0.1:5000/validate_test"
#####
@app.route('/extract_size', methods=['POST'])
def extract_size():
    try:
        body = request.get_json()
        print(body)
        size = module_1._extractSize(body)
        return size
        # return 'Please see results in folder /static/batch_images/validate_result'
    except:
        return IMAGE_NAME_ERROR