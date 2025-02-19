from flask_cors import CORS
from bson.objectid import ObjectId
import gridfs
from io import BytesIO

import base64
import os


from flask import Flask, render_template, redirect, url_for, session, flash,jsonify, send_file,request
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


uri = os.getenv("MONGO_URI")


client = None
db = None
fs= None

try:
    if not uri:
        raise Exception("MONGO_URI not loaded from environment variables.")

    client = MongoClient(uri, server_api=ServerApi('1'))
    db = client["songRq"]

    if not db:
        raise Exception("Failed to initialize the database.")

    lost_found_collection = db.lost_found
    fs = gridfs.GridFS(db)

    print("Debug: MongoDB connected successfully.") 

except Exception as e:
    print(f"Error: Database connection failed: {e}")
    client = None  #


app = Flask(__name__)
CORS(app)  


@app.route('/')
def home():
    print("Home")

    return render_template('index.html')



def report_lost():
    title = request.form.get("title")
    description = request.form.get("description")
    image = request.files.get("image")  

    if not title or not description:
        return jsonify({"error": "Title and description are required"}), 400
    
    image_id = None
    if image:
        image_id = fs.put(image.read(), filename=image.filename)  

    report = {
        "title": title,
        "description": description,
        "image_id": str(image_id) if image_id else None
    }
    report_id = lost_found_collection.insert_one(report).inserted_id

    return jsonify({"message": "Lost item reported successfully!", "id": str(report_id)}), 201

@app.route('/api/report-found', methods=['POST'])
def report_found():
    data = request.json  
    if not data:
        return jsonify({"error": "Invalid data"}), 400  

    #llist images of the lost item
    print("Received found report:", data)




@app.route('/api/login', methods=['POST'])
def login():
    data = request.json  
    if not data:
        return jsonify({"error": "Invalid data"}), 400  

    print("Received login data:", data)

    username = request.form.get("username")
    password = request.form.get("password")


    if not lost_found_collection.find_one({"username": username, "password": password}):
        return jsonify({"error": "Invalid credentials"}), 401
    

    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
