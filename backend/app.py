from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from engine import generate_timetable
from excel_parser import parse_excel_to_config
from database import init_db, save_timetable, get_all_timetables, get_timetable_by_id, delete_timetable, delete_all_timetables

app = Flask(__name__)
CORS(app) # Enable Cross-Origin Resource Sharing

# Ensure we have a place to store temp uploads
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Initialize database
init_db()

@app.route('/api/upload-schedule', methods=['POST'])
def upload_schedule():
    """
    1. Receives an Excel file.
    2. Parses it into JSON structure.
    3. Runs the Optimization Engine.
    4. Returns the Schedule.
    """
    # 1. Check if file is present
    if 'file' not in request.files:
        return jsonify({"status": "error", "message": "No file part"}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"status": "error", "message": "No selected file"}), 400

    filepath = None
    try:
        # 2. Save file temporarily
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)
        
        print(f"Processing file: {filepath}")

        # 3. Parse Excel -> JSON Config
        config_data = parse_excel_to_config(filepath)
        
        # 4. Run Optimization Engine
        # The engine now takes the data directly from the parser output
        result = generate_timetable(config_data)
        
        # 5. Cleanup (Delete the temp file)
        if os.path.exists(filepath):
            os.remove(filepath)
            
        return jsonify(result)

    except Exception as e:
        print(f"Error processing request: {e}")
        # Clean up file if error occurs
        if filepath and os.path.exists(filepath):
            os.remove(filepath)
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Simple route to check if server is running"""
    return jsonify({"status": "online", "message": "Scheduler API is ready"})

@app.route('/api/save-timetable', methods=['POST'])
def save_schedule():
    """
    Save a generated timetable to the database
    This will delete all previous timetables and save each class as a separate timetable
    Expects JSON body with:
    - schedule_data: The timetable schedule (can contain multiple classes)
    - department: Department name (optional, default: CSE)
    - semester: Semester info (optional)
    - academic_year: Academic year (optional)
    - file_name: Original file name (optional)
    """
    try:
        data = request.get_json()
        
        if not data or 'schedule_data' not in data:
            return jsonify({"status": "error", "message": "Missing schedule data"}), 400
        
        schedule_data = data['schedule_data']
        department = data.get('department', 'CSE')
        semester = data.get('semester')
        academic_year = data.get('academic_year')
        file_name = data.get('file_name')
        
        # Delete all previous timetables from the same department
        delete_all_timetables(department=department)
        
        # Save each class as a separate timetable
        saved_ids = []
        for class_name, class_schedule in schedule_data.items():
            # Create individual schedule data for this class
            individual_schedule = {class_name: class_schedule}
            
            # Prepare metadata
            metadata = {
                'total_classes': 1,
                'file_name': file_name,
                'created_by': 'Admin'
            }
            
            # Save to database
            timetable_id = save_timetable(
                schedule_data=individual_schedule,
                department=department,
                semester=class_name,  # Use class name as semester identifier
                academic_year=academic_year,
                metadata=metadata
            )
            saved_ids.append(timetable_id)
        
        return jsonify({
            "status": "success",
            "message": f"Successfully saved {len(saved_ids)} class timetables",
            "timetable_ids": saved_ids
        }), 200
    
    except Exception as e:
        print(f"Error saving timetable: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/timetables', methods=['GET'])
def get_timetables():
    """
    Get all saved timetables
    Query params:
    - department: Filter by department (optional)
    - limit: Maximum number of results (default: 50)
    """
    try:
        department = request.args.get('department')
        limit = int(request.args.get('limit', 50))
        
        timetables = get_all_timetables(department=department, limit=limit)
        
        return jsonify({
            "status": "success",
            "count": len(timetables),
            "timetables": timetables
        }), 200
    
    except Exception as e:
        print(f"Error fetching timetables: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/timetable/<int:timetable_id>', methods=['GET'])
def get_single_timetable(timetable_id):
    """Get a specific timetable by ID"""
    try:
        timetable = get_timetable_by_id(timetable_id)
        
        if timetable:
            return jsonify({
                "status": "success",
                "timetable": timetable
            }), 200
        else:
            return jsonify({
                "status": "error",
                "message": "Timetable not found"
            }), 404
    
    except Exception as e:
        print(f"Error fetching timetable: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/timetable/<int:timetable_id>', methods=['DELETE'])
def remove_timetable(timetable_id):
    """Delete a timetable by ID"""
    try:
        success = delete_timetable(timetable_id, soft_delete=True)
        
        if success:
            return jsonify({
                "status": "success",
                "message": "Timetable deleted successfully"
            }), 200
        else:
            return jsonify({
                "status": "error",
                "message": "Failed to delete timetable"
            }), 400
    
    except Exception as e:
        print(f"Error deleting timetable: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/timetables/delete-all', methods=['DELETE'])
def remove_all_timetables():
    """Delete all timetables"""
    try:
        success = delete_all_timetables()
        
        if success:
            return jsonify({
                "status": "success",
                "message": "All timetables deleted successfully"
            }), 200
        else:
            return jsonify({
                "status": "error",
                "message": "Failed to delete timetables"
            }), 400
    
    except Exception as e:
        print(f"Error deleting all timetables: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)