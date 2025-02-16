from flask import Flask, request, jsonify
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)  


@app.route('/api/report-lost', methods=['POST'])
def report_lost():
    data = request.json 
    if not data:
        return jsonify({"error": "Invalid data"}), 400  


    print("Received lost report:", data)



    return jsonify({"message": "Lost item reported successfully!"}), 201

@app.route('/api/report-found', methods=['POST'])
def report_found():
    data = request.json  
    if not data:
        return jsonify({"error": "Invalid data"}), 400  

    print("Received lost report:", data)



    return jsonify({"message": "Lost item reported successfully!"}), 201


if __name__ == '__main__':
    app.run(debug=True)
