from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity
from datetime import timedelta
import os
from engine import generate_timetable
from excel_parser import parse_excel_to_config
from database import init_db, save_timetable, get_all_timetables, get_timetable_by_id, delete_timetable, delete_all_timetables, update_teacher_password
from auth import authenticate_teacher, teacher_required, get_current_teacher, check_password, hash_password

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


@app.route('/api/staff-timetables', methods=['GET'])
def get_staff_timetables():
    """
    Get individual timetables for all staff members.
    Extracts staff names from all timetables and builds their individual schedules.
    Returns staff list with their periods per week and detailed schedule.
    """
    try:
        import re
        
        def normalize_staff_name(name):
            """Normalize name: remove ALL spaces, lowercase"""
            if not name or not isinstance(name, str):
                return ""
            # Add space after periods then remove all spaces
            name = re.sub(r'\.(?=[A-Za-z])', '. ', name)
            return name.lower().replace(' ', '')

        # Get all timetables
        all_timetables = get_all_timetables(limit=1000)

        if not all_timetables:
            return jsonify({
                "status": "success",
                "staff_timetables": [],
                "total_staff": 0
            }), 200

        # Dictionary to store each staff's schedule
        staff_schedules = {}

        # Day mapping
        day_names = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']

        for timetable in all_timetables:
            schedule_data = timetable['schedule_data']

            for class_name, class_schedule in schedule_data.items():
                for day_idx, day_name in enumerate(day_names):
                    day_schedule = class_schedule.get(day_name, [])

                    for period_idx, period_entry in enumerate(day_schedule):
                        # Skip free periods
                        if period_entry == '-- FREE --' or not period_entry:
                            continue

                        # Extract staff names from period entry
                        # Format: "Subject (Staff1 & Staff2)" or "[LAB] Subject (Staff1 & Staff2)"
                        match = re.search(r'\(([^)]+)\)$', period_entry)
                        if match:
                            staff_str = match.group(1)
                            # Split by & or / for multiple staff
                            staff_names = [s.strip() for s in re.split(r'\s*[&/]\s*', staff_str)]

                            # Extract subject name (remove [LAB], [TUT], [INT-LAB] prefixes)
                            subject = re.sub(r'^\[(LAB|TUT|INT-LAB)\]\s*', '', period_entry)
                            subject = re.sub(r'\s*\([^)]+\)$', '', subject).strip()

                            for staff_name in staff_names:
                                if not staff_name:
                                    continue

                                # Normalize for deduplication but keep original display name
                                staff_normalized = normalize_staff_name(staff_name)
                                
                                # Initialize staff entry if not exists
                                if staff_normalized not in staff_schedules:
                                    staff_schedules[staff_normalized] = {
                                        'name': staff_name,  # Use first occurrence's display name
                                        'periods': [],
                                        'schedule': {day: [None] * 7 for day in day_names},
                                        'periods_per_week': 0,
                                        'classes': set(),
                                        'subjects': set()
                                    }

                                # Add period info
                                staff_schedules[staff_normalized]['periods'].append({
                                    'day': day_idx,
                                    'day_name': day_name,
                                    'period': period_idx,
                                    'class': class_name,
                                    'subject': subject,
                                    'full_entry': period_entry
                                })

                                # Update schedule grid
                                existing = staff_schedules[staff_normalized]['schedule'][day_name][period_idx]
                                new_entry = f"{class_name}: {subject}"
                                if existing:
                                    # Multiple classes at same time (shouldn't happen but handle it)
                                    staff_schedules[staff_normalized]['schedule'][day_name][period_idx] = f"{existing} | {new_entry}"
                                else:
                                    staff_schedules[staff_normalized]['schedule'][day_name][period_idx] = new_entry

                                staff_schedules[staff_normalized]['classes'].add(class_name)
                                staff_schedules[staff_normalized]['subjects'].add(subject)

        # Convert to list and calculate totals
        staff_list = []
        for staff_name, data in staff_schedules.items():
            staff_list.append({
                'name': data['name'],
                'periods_per_week': len(data['periods']),
                'schedule': data['schedule'],
                'periods': data['periods'],
                'classes': list(data['classes']),
                'subjects': list(data['subjects']),
                'total_classes': len(data['classes']),
                'total_subjects': len(data['subjects'])
            })

        # Sort by name
        staff_list.sort(key=lambda x: x['name'])

        return jsonify({
            "status": "success",
            "staff_timetables": staff_list,
            "total_staff": len(staff_list)
        }), 200

    except Exception as e:
        print(f"Error fetching staff timetables: {e}")
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
        import re
        
        def normalize_staff_name(name):
            """Normalize name: remove ALL spaces, lowercase"""
            if not name or not isinstance(name, str):
                return ""
            # Add space after periods then remove all spaces
            name = re.sub(r'\.(?=[A-Za-z])', '. ', name)
            return name.lower().replace(' ', '')
        
        teacher = get_current_teacher()

        if not teacher:
            return jsonify({"status": "error", "message": "Teacher not found"}), 404

        teacher_name = teacher['name']
        teacher_name_normalized = normalize_staff_name(teacher_name)

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
                        # Extract staff names from period entry for exact matching
                        # Format: "Subject (Staff1 & Staff2)" or "[LAB] Subject (Staff1 & Staff2)"
                        if period and period != '-- FREE --':
                            match = re.search(r'\(([^)]+)\)$', period)
                            if match:
                                staff_str = match.group(1)
                                # Split by & or / for multiple staff
                                period_staff_names = [s.strip() for s in re.split(r'\s*[&/]\s*', staff_str)]
                                # Normalize all period staff names for comparison
                                period_staff_normalized = [normalize_staff_name(s) for s in period_staff_names]
                                
                                # Check if teacher name matches any staff in this period (normalized)
                                if teacher_name_normalized in period_staff_normalized:
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


@app.route('/api/teacher/change-password', methods=['POST'])
@teacher_required
def change_teacher_password():
    """
    Change password for the logged-in teacher
    """
    try:
        teacher = get_current_teacher()

        if not teacher:
            return jsonify({"status": "error", "message": "Teacher not found"}), 404

        data = request.get_json()
        current_password = data.get('currentPassword')
        new_password = data.get('newPassword')

        if not current_password or not new_password:
            return jsonify({"status": "error", "message": "Both current and new passwords are required"}), 400

        # Verify current password
        if not check_password(current_password, teacher['password_hash']):
            return jsonify({"status": "error", "message": "Current password is incorrect"}), 401

        # Hash new password
        new_password_hash = hash_password(new_password)

        # Update password in database
        success = update_teacher_password(teacher['id'], new_password_hash)

        if success:
            return jsonify({"status": "success", "message": "Password changed successfully"}), 200
        else:
            return jsonify({"status": "error", "message": "Failed to update password"}), 500

    except Exception as e:
        print(f"Error changing password: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)