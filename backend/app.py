from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
from engine import generate_timetable

app = Flask(__name__)
CORS(app) # Enable Cross-Origin Resource Sharing to allow React to talk to Flask

DATA_FILE = 'data.json'

def load_data():
    """Helper to read data from the JSON file."""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {} # Return empty if file is corrupted
    return {}

def save_data(data):
    """Helper to write data to the JSON file."""
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

@app.route('/api/data', methods=['GET', 'POST'])
def handle_data():
    """
    GET: Returns the current department configuration.
    POST: Updates and saves the department configuration.
    """
    if request.method == 'GET':
        data = load_data()
        return jsonify(data)
    
    elif request.method == 'POST':
        data = request.json
        if not data:
             return jsonify({"status": "error", "message": "No data provided"}), 400
        
        save_data(data)
        return jsonify({"status": "success", "message": "Configuration saved successfully"})

@app.route('/api/generate', methods=['POST'])
def generate():
    """
    Trigger the scheduling engine.
    Expects the full configuration JSON in the request body.
    """
    data = request.json
    print("Received request to generate schedule...")
    
    if not data:
        return jsonify({"status": "error", "message": "No data provided for generation"}), 400

    try:
        # Run the two-step optimization engine
        result = generate_timetable(data)
        return jsonify(result)
    except Exception as e:
        print(f"Critical Error during generation: {e}")
        # Return a 500 error so the frontend knows something went wrong
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    # Run the server on port 5000
    app.run(debug=True, port=5000)