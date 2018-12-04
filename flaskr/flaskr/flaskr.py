# all the imports
import os
import os.path
import sqlite3
import csv
import json
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash

app = Flask(__name__) # create the application instance
app.config.from_object(__name__) # load config from this file , flaskr.py

from mongoengine import *
connect('MongoDB')

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'flaskr.db'),
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

#Creating the Database model for cellphone
class CellPhone(Document):
    Country = StringField(max_length=255)
    year = DictField()

#Reading Cellphone Data from CSV
def create_phone():
    
    #Array that holds Cellphone data
    activeCellPhone = []
    if os.path.exists('data/cellphone.csv') == True:
        print("CSV found!");
    else:
        print("Cannot read CSV");

    with open('data/cellphone.csv') as File:
        reader = csv.DictReader(File, delimiter=',', quotechar=',',
                            quoting=csv.QUOTE_MINIMAL)
        for line in reader:
            tempCountry = line["Country"]
            datayear = {}
            for year in range(1990,2012):
                year = str(year)
                tempyear = "y" + year
                datayear[tempyear] = line[tempyear]
            cell = CellPhone(Country=tempCountry, year=datayear).save()
            activeCellPhone.append(cell)
    return activeCellPhone

#ToJsonData
@app.route('/jsondata')
def tojson():
    cellData = CellPhone.objects
    return cellData.to_json()

#HomePage
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

#DataPage
@app.route('/ref')
def data():
    return render_template('ref.html')

#inspirationsPage
@app.route('/inspirations')
def inspirations():
    return render_template('inspirations.html')

#Loading Data Page
@app.route('/loadData')
def loadingData():
    activeCellPhone = create_phone()
    return render_template('home.html')

#Error Checker
@app.route('/404check')
def errorCheck():
    abort(404)
    return render_template('home.html')

#Error Handlers
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(403)
def page_not_found(e):
    return render_template('403.html'), 403

@app.errorhandler(410)
def page_not_found(e):
    return render_template('410.html'), 410

@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500