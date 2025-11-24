from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity
from datetime import timedelta
import os
from engine import generate_timetable
from excel_parser import parse_excel_to_config
from database import init_db, save_timetable, get_all_timetables, get_timetable_by_id, delete_timetable, delete_all_timetables
from auth import authenticate_teacher, teacher_required, get_current_teacher

app = Flask(__name__)
CORS(app) # Enable Cross-Origin Resource Sharing

# JWT Configuration
app.config['JWT_SECRET_KEY'] = 'skeduler-secret-key-change-in-production'  # Change this in production!
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)
app.config['JWT_TOKEN_LOCATION'] = ['headers']
app.config['JWT_HEADER_NAME'] = 'Authorization'
app.config['JWT_HEADER_TYPE'] = 'Bearer'
jwt = JWTManager(app)

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

# ==================== TEACHER AUTHENTICATION ENDPOINTS ====================

@app.route('/api/teacher/login', methods=['POST'])
def teacher_login():
    """
    Authenticate teacher and return JWT token
    Expects JSON body with: username, password
    """
    try:
        data = request.get_json()

        if not data or 'username' not in data or 'password' not in data:
            return jsonify({"status": "error", "message": "Username and password required"}), 400

        username = data['username']
        password = data['password']

        # Authenticate teacher
        teacher = authenticate_teacher(username, password)

        if teacher:
            # Create JWT token (convert ID to string for JWT compatibility)
            access_token = create_access_token(identity=str(teacher['id']))

            return jsonify({
                "status": "success",
                "message": "Login successful",
                "access_token": access_token,
                "teacher": teacher
            }), 200
        else:
            return jsonify({
                "status": "error",
                "message": "Invalid username or password"
            }), 401

    except Exception as e:
        print(f"Error during login: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/api/teacher/profile', methods=['GET'])
@teacher_required
def get_teacher_profile():
    """Get the logged-in teacher's profile"""
    try:
        teacher = get_current_teacher()

        if teacher:
            return jsonify({
                "status": "success",
                "teacher": teacher
            }), 200
        else:
            return jsonify({"status": "error", "message": "Teacher not found"}), 404

    except Exception as e:
        print(f"Error fetching profile: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/api/teacher/timetable', methods=['GET'])
@teacher_required
def get_teacher_timetable():
    """
    Get timetable for the logged-in teacher
    Returns all periods where the teacher is assigned
    """
    try:
        teacher = get_current_teacher()

        if not teacher:
            return jsonify({"status": "error", "message": "Teacher not found"}), 404

        teacher_name = teacher['name']

        # Get all timetables
        all_timetables = get_all_timetables(limit=1000)

        # Filter and extract periods where this teacher is assigned
        teacher_schedule = {}

        for timetable in all_timetables:
            schedule_data = timetable['schedule_data']

            for class_name, class_schedule in schedule_data.items():
                # Check if teacher has any periods in this class
                teacher_periods = []

                for day_idx in range(6):  # 6 days
                    day_key = str(day_idx) if isinstance(list(class_schedule.keys())[0], str) else day_idx
                    day_schedule = class_schedule.get(day_key, class_schedule.get(str(day_idx), []))

                    for period_idx, period in enumerate(day_schedule):
                        if teacher_name in period:
                            teacher_periods.append({
                                'day': day_idx,
                                'period': period_idx,
                                'subject': period
                            })

                if teacher_periods:
                    teacher_schedule[class_name] = {
                        'periods': teacher_periods,
                        'full_schedule': class_schedule,
                        'timetable_id': timetable['id'],
                        'department': timetable['department'],
                        'academic_year': timetable.get('academic_year')
                    }

        return jsonify({
            "status": "success",
            "teacher": teacher,
            "schedule": teacher_schedule,
            "total_classes": len(teacher_schedule)
        }), 200

    except Exception as e:
        print(f"Error fetching teacher timetable: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)