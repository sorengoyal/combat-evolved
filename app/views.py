from flask import render_template, flash, redirect, request
from app import app
from app.plab.geospatial import Geospatial
import json
import app.compute as compute
@app.route('/')
def index():
    return render_template('base.html', key = 'AIzaSyCdlOuxf56nB-hgN35Jpvk7qm7px-8wCPA')

@app.route('/polygon', methods=['POST'])
def receive():
    polygon = request.get_json()
    pre_coordinates = [ [point["lng"], point["lat"]] for point in polygon["polygon"] ]
    pre_coordinates.append(pre_coordinates[0])
    coordinates = [  pre_coordinates ] #Planet api demands a complete loop of coordinates
    compute.ndviImages(coordinates)
    return render_template('base.html', key = 'AIzaSyCdlOuxf56nB-hgN35Jpvk7qm7px-8wCPA')
