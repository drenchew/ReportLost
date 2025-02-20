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
    db = client["LostFound"]

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


@app.route('/api/report-lost', methods=['POST'])
def report_lost():
    title = request.form.get("item")
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

@app.route('/api/report-found', methods=['GET'])
def report_found():
    data = list(lost_found_collection.find({}))

    if not data:
        return jsonify([]), 200  # Return empty array instead of error

    for item in data:
        item["_id"] = str(item["_id"])  # Convert MongoDB ObjectId to string
        item["imageUrl"] = f"http://127.0.0.1:5000/api/image/{item['image_id']}" if item.get("image_id") else None  # Generate image URL

    return jsonify(data), 200

# 🔹 Route to serve images from GridFS
@app.route('/api/image/<image_id>', methods=['GET'])
def get_image(image_id):
    try:
        image = fs.get(ObjectId(image_id))
        return send_file(BytesIO(image.read()), mimetype="image/png")  # Adjust MIME type if needed
    except Exception:
        return jsonify({"error": "Image not found"}), 404
        




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
