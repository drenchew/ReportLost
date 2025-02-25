from flask import Flask, render_template, redirect, url_for, session, jsonify, request, send_file
from flask_cors import CORS
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson.objectid import ObjectId
import gridfs
import bcrypt
import os
from io import BytesIO
from datetime import timedelta




uri = os.getenv("MONGO_URI")
secret_key = os.getenv("SECRET_KEY") or "default_secret_key"


client = None
db = None
fs = None

try:
    if not uri:
        raise Exception("MONGO_URI not loaded from environment variables.")

    client = MongoClient(uri, server_api=ServerApi('1'))
    db = client["LostFound"]

    if not db:
        raise Exception("Failed to initialize the database.")

    lost_found_collection = db.lost_found
    credentials_collection = db.credentials
    fs = gridfs.GridFS(db)

    print("✅ MongoDB connected successfully.") 

except Exception as e:
    print(f"Error: Database connection failed: {e}")
    client = None  

# Flask App
app = Flask(__name__)
app.secret_key = secret_key

from datetime import timedelta
app.permanent_session_lifetime = timedelta(minutes=30)  



app.config["SESSION_COOKIE_NAME"] = "session_id"
app.config["SESSION_COOKIE_HTTPONLY"] = True  
app.config["SESSION_COOKIE_SECURE"] = False   #true for https
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"  
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(days=1)

CORS(app, supports_credentials=True) 




@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/report-lost', methods=['POST', 'GET'])
def report_lost():
    if request.method == 'GET':
        return jsonify({"message": "Log in to report lost item"}), 200

  
    
    user = session["username"]
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
        "image_id": str(image_id) if image_id else None,
        "username": user,
    }

    report_id = lost_found_collection.insert_one(report).inserted_id
    return jsonify({"message": "Lost item reported successfully!", "id": str(report_id)}), 201

@app.route('/api/report-found', methods=['GET'])
def report_found():
    data = list(lost_found_collection.find({}))
    if not data:
        return jsonify([]), 200  

    for item in data:
        item["_id"] = str(item["_id"])  
        item["imageUrl"] = f"http://127.0.0.1:5000/api/image/{item['image_id']}" if item.get("image_id") else None  

    return jsonify(data), 200

@app.route('/api/image/<image_id>', methods=['GET'])
def get_image(image_id):
    try:
        image = fs.get(ObjectId(image_id))
        return send_file(BytesIO(image.read()), mimetype="image/png")  
    except Exception:
        return jsonify({"error": "Image not found"}), 404

@app.route('/api/delete/<id>', methods=['DELETE'])
def delete_post(id):
    session["username"] = "Aadmin"
    if "username" not in session:
        return jsonify({"error": "Unauthorized"}), 401 
    
    post = lost_found_collection.find_one({"_id": ObjectId(id)})
    if not post:
        return jsonify({"error": "Post not found"}), 404

    if post["username"] != session["username"]:
        return jsonify({"error": "You can only delete your own posts"}), 403  

    lost_found_collection.delete_one({"_id": ObjectId(id)})
    return jsonify({"message": "Post deleted successfully"}), 200

@app.route('/api/register', methods=['POST'])
def register():
    username = request.form.get("username")
    password = request.form.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400
    
    if credentials_collection.find_one({"username": username}):
        return jsonify({"error": "Username already exists"}), 400

    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    credentials_collection.insert_one({"username": username, "password": hashed_password})
    
    session['username'] = username  

    return jsonify({"message": "User registered successfully!"}), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")


  

    user = credentials_collection.find_one({"username": username})
    if not user:
        return jsonify({"error": "Invalid credentials"}), 401

    if not bcrypt.checkpw(password.encode("utf-8"), user["password"]):
        return jsonify({"error": "Invalid credentials"}), 401

    session.permanent = True
    session['username'] = username  
    return jsonify({"message": "Login successful!"}), 200

@app.route('/api/logout', methods=['POST'])
def logout():
    session.pop("username", None)  
    return jsonify({"message": "Logged out successfully"}), 200

@app.route('/api/session', methods=['GET'])
def get_session():
   
    if "username" in session:

        return jsonify({"username": session["username"]}), 200
    return jsonify({"error": "Not logged in"}), 401

if __name__ == '__main__':
    app.run(debug=True)
