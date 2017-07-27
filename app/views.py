from flask import render_template, flash, redirect, request, send_file, jsonify
from app import app
import json
import logging
import app.compute as compute
#import os

logger = logging.getLogger("root."+ __name__)


@app.route('/')
def index():
    return render_template('base.html', key = 'AIzaSyAbRZJg6qxBQ3q3Q4ojVuDYyTkOoxsIhxw')

@app.route('/polygon', methods=['POST'])
def receive():
    polygon = request.get_json()
    pre_coordinates = [ [point["lng"], point["lat"]] for point in polygon["polygon"] ]
    pre_coordinates.append(pre_coordinates[0])
    coordinates = [  pre_coordinates ] #Planet api demands a complete loop of coordinates
    #compute.ndviImages(coordinates)
    #return render_template('base.html', key = 'AIzaSyCdlOuxf56nB-hgN35Jpvk7qm7px-8wCPA')
    return jsonify({"Message":"Downloaded Image Sucessfully"})

@app.route('/poll', methods=['GET'])
def poll():
    response = {"status": 0}
    print(os.getcwd())
    try:
        for i in range(1,2):
            open('app/images/file' + str(i) + '.png', 'r')
            response["status"] = response["status"] + 25
    except FileNotFoundError as err:
        print(err.filename)
        logger.info("poll(): Could not find - " + err.filename)
    logger.debug("poll(): response sent - " + str(response["status"]))
    return jsonify(response)

@app.route('/file0.png', methods=['GET'])
def getImage():
#    if request.args.get('type') == '1':
#       filename = 'ok.gif'
#    else:
#       filename = 'error.gif'
    return send_file('images/file0.png', mimetype='image/png')

@app.route('/graph.png', methods=['GET'])
def getGraph():
#    if request.args.get('type') == '1':
#       filename = 'ok.gif'
#    else:
#       filename = 'error.gif'
    return send_file('images/graph.png', mimetype='image/png')

