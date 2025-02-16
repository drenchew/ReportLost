from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow requests from React frontend

# Report Lost Route
@app.route('/api/report-lost', methods=['POST'])
def report_lost():
    data = request.json  # Get JSON data from frontend
    if not data:
        return jsonify({"error": "Invalid data"}), 400  # Return error if no data

    # Example: Save data to a database (not implemented here)
    print("Received lost report:", data)

    return jsonify({"message": "Lost item reported successfully!"}), 201

if __name__ == '__main__':
    app.run(debug=True)
