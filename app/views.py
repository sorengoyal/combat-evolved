from flask import render_template, flash, redirect, request
from app import app

@app.route('/')
def index():
    return render_template('base.html', key = 'AIzaSyCdlOuxf56nB-hgN35Jpvk7qm7px-8wCPA')

@app.route('/polygon', methods=['POST'])
def receive():
    print(request.get_json())
    return render_template('base.html', key = 'AIzaSyCdlOuxf56nB-hgN35Jpvk7qm7px-8wCPA')
