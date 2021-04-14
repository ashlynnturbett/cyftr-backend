import os

import flask_cors
from flask import Flask, flash, request, redirect, url_for, session, send_from_directory, make_response, jsonify, \
    send_file
from werkzeug.utils import secure_filename
from flask_cors import CORS, cross_origin
import logging

import csv
import json

from cyftr import databaseFunction

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger('HELLO WORLD')


#hardcoded to file on Ashlynn's computer
UPLOAD_FOLDER = r'C:\Users\suzie\Documents\cyftr2\save'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','csv'])

app = Flask(__name__, static_folder='../build', static_url_path='/')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# @app.route('/')
# def index():
#     return app.send_static_file('index.html')

@app.route('/upload', methods=['POST'])
@cross_origin(origin = '*')
def fileUpload():
    target=os.path.join(UPLOAD_FOLDER,'test_docs')
    if not os.path.isdir(target):
        os.mkdir(target)
    logger.info("welcome to upload`")
    file = request.files['file']
    filename = secure_filename(file.filename)
    print(filename)
    destination="/".join([target, filename])
    file.save(destination)
    session['uploadFilePath']=destination

    databaseFunction.verifyList(filename)

    # Decide the two file paths according to your
    # computer system
    csvFilePath = r'C:\Users\suzie\Documents\cyftr2\ResidentData_Results.csv'
    jsonFilePath = r'C:\Users\suzie\Documents\cyftr2\response.json'

    make_json(csvFilePath, jsonFilePath)

    return send_file(jsonFilePath)
    # return send_from_directory(r'C:\Users\suzie\Documents\cyftr2\save\test_docs', filename)


def make_json(csvFilePath, jsonFilePath):
    jsonArray = []

    # read csv file
    with open(csvFilePath, encoding='utf-8') as csvf:
        # load csv file data using csv library's dictionary reader
        csvReader = csv.DictReader(csvf)

        # convert each csv row into python dict
        for row in csvReader:
            # add this python dict to json array
            jsonArray.append(row)

    # convert python jsonArray to JSON String and write to file
    with open(jsonFilePath, 'w', encoding='utf-8') as jsonf:
        jsonString = json.dumps(jsonArray, indent=4)
        jsonf.write(jsonString)

if __name__ == "__main__":
    app.secret_key = os.urandom(24)
    app.run(debug=True,host="0.0.0.0",use_reloader=False)

flask_cors.CORS(app, expose_headers='Authorization')
