from flask import Flask, render_template, request, Response, send_file
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from werkzeug import secure_filename
import pandas
from geopy.geocoders import Nominatim
import os


app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:standardna18ka@localhost/geo-coder'   #configuring the database connection; with the one I create in pg4
db=SQLAlchemy(app) #creats an SQL alchemy object

#for future: you need to create the db by importing 'from geocoder import db' and then running db.create_all() in cmd

class Data(db.Model): #blueprint of a database already created in SQLAlchemy and then accessing the model
    __tablename__="submitted_data"
    id=db.Column(db.Integer, primary_key=True) #setting the id primary primary_key
    address_=db.Column(db.String(250), unique=True) #creating an email column with 120 limit and requiring only unique values
    name_=db.Column(db.String(100))
    employees_=db.Column(db.Integer)
    lattitude_=db.Column(db.Integer)
    longitude_=db.Column(db.Integer)

@app.route("/")
def index():
    return render_template("index.html")


#TO DO:
#files-uploading-and downloading works like a charm!!!
#connect the project to github and work on it from there as well.
#Go through tutorials and find where he manipulates files and creates longitude and lattitude from CSV
#make it look nice through some peachy css


@app.route("/processed-uploaded-data", methods=['POST']) #to REDO REDO
def processed_data():
    global file
    if request.method=='POST':
       file=request.files["file"]
       #file.save(secure_filename("uploaded"+file.filename))
    nom=Nominatim(scheme="http")
    df=pandas.read_csv(file)
    df["Coordinates"]=df["Address"].apply(nom.geocode)
    df["Latitude"]=df["Coordinates"].apply(lambda x: x.latitude if x != None else None)
    df["Longitude"]=df["Coordinates"].apply(lambda x: x.longitude if x != None else None)
    df.drop("Coordinates", axis=1, inplace=True)

    return render_template("success.html")

@app.route("/download", methods=['POST', 'GET'])
def download():
    return send_file(file, attachment_filename="processed-file.csv", as_attachment=True)

if __name__=='__main__':
    app.debug=True
    app.run(port=5050)
