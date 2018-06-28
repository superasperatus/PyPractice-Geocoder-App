from flask import Flask, render_template, request, Response, send_file
import pandas
from geopy.geocoders import Nominatim


app=Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/processed-uploaded-data", methods=['POST']) #to REDO REDO
def processed_data():
    global upl_file
    if request.method=='POST':
       upl_file=request.files["file"]
    nom=Nominatim(scheme="http")
    df=pandas.read_csv(upl_file)
    df["Coordinates"]=df["Address"].apply(nom.geocode)
    df["Latitude"]=df["Coordinates"].apply(lambda x: x.latitude if x != None else 'Cannot Read Address Format')
    df["Longitude"]=df["Coordinates"].apply(lambda x: x.longitude if x != None else 'Cannot Read Address Format')
    df.drop("Coordinates", axis=1, inplace=True)
    return render_template("success.html")


@app.route("/download", methods=['POST', 'GET'])
def download():
    return send_file(upl_file, attachment_filename="processed-file.csv", as_attachment=True)

if __name__=='__main__':
    app.debug=True
    app.run(port=5050)
