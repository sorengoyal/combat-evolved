from flask import render_template, flash, redirect
from app import app

@app.route('/')
def index():
    return render_template('index.html', key = 'AIzaSyCdlOuxf56nB-hgN35Jpvk7qm7px-8wCPA')
