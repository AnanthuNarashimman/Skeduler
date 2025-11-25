import sqlite3
import json
from datetime import datetime
import os

DATABASE_PATH = 'timetable.db'

def get_db_connection():
    """Create a database connection"""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row  # Return rows as dictionaries
    return conn

def init_db():
    """Initialize the database with required tables"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create timetables table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS timetables (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            department TEXT NOT NULL,
            semester TEXT,
            academic_year TEXT,
            schedule_data TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_active INTEGER DEFAULT 1
        )
    ''')
    
    # Create timetable_metadata table for additional info
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS timetable_metadata (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timetable_id INTEGER NOT NULL,
            total_classes INTEGER,
            total_subjects INTEGER,
            file_name TEXT,
            created_by TEXT,
            FOREIGN KEY (timetable_id) REFERENCES timetables (id) ON DELETE CASCADE
        )
    ''')

    # Create teachers table for authentication
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS teachers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            email TEXT,
            department TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_active INTEGER DEFAULT 1
        )
    ''')

    conn.commit()
    conn.close()
    print("Database initialized successfully!")

def save_timetable(schedule_data, department="CSE", semester=None, academic_year=None, metadata=None):
    """
    Save a timetable to the database
    
    Args:
        schedule_data (dict): The complete schedule data
        department (str): Department name
        semester (str): Semester information
        academic_year (str): Academic year
        metadata (dict): Additional metadata like file_name, total_classes, etc.
    
    Returns:
        int: The ID of the saved timetable
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Convert schedule data to JSON string
        schedule_json = json.dumps(schedule_data)
        
        # Insert into timetables table
        cursor.execute('''
            INSERT INTO timetables (department, semester, academic_year, schedule_data)
            VALUES (?, ?, ?, ?)
        ''', (department, semester, academic_year, schedule_json))
        
        timetable_id = cursor.lastrowid
        
        # Insert metadata if provided
        if metadata:
            cursor.execute('''
                INSERT INTO timetable_metadata 
                (timetable_id, total_classes, total_subjects, file_name, created_by)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                timetable_id,
                metadata.get('total_classes'),
                metadata.get('total_subjects'),
                metadata.get('file_name'),
                metadata.get('created_by', 'Admin')
            ))
        
        conn.commit()
        return timetable_id
    
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def get_timetable_by_id(timetable_id):
    """Retrieve a timetable by its ID"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT t.*, tm.total_classes, tm.total_subjects, tm.file_name, tm.created_by
        FROM timetables t
        LEFT JOIN timetable_metadata tm ON t.id = tm.timetable_id
        WHERE t.id = ?
    ''', (timetable_id,))
    
    row = cursor.fetchone()
    conn.close()
    
    if row:
        result = dict(row)
        result['schedule_data'] = json.loads(result['schedule_data'])
        return result
    return None

def get_all_timetables(department=None, limit=50):
    """Retrieve all timetables, optionally filtered by department"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if department:
        cursor.execute('''
            SELECT t.*, tm.total_classes, tm.file_name
            FROM timetables t
            LEFT JOIN timetable_metadata tm ON t.id = tm.timetable_id
            WHERE t.department = ? AND t.is_active = 1
            ORDER BY t.created_at DESC
            LIMIT ?
        ''', (department, limit))
    else:
        cursor.execute('''
            SELECT t.*, tm.total_classes, tm.file_name
            FROM timetables t
            LEFT JOIN timetable_metadata tm ON t.id = tm.timetable_id
            WHERE t.is_active = 1
            ORDER BY t.created_at DESC
            LIMIT ?
        ''', (limit,))
    
    rows = cursor.fetchall()
    conn.close()
    
    results = []
    for row in rows:
        item = dict(row)
        item['schedule_data'] = json.loads(item['schedule_data'])
        results.append(item)
    
    return results

def delete_timetable(timetable_id, soft_delete=True):
    """
    Delete a timetable
    
    Args:
        timetable_id (int): ID of the timetable to delete
        soft_delete (bool): If True, mark as inactive; if False, permanently delete
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        if soft_delete:
            cursor.execute('''
                UPDATE timetables
                SET is_active = 0, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (timetable_id,))
        else:
            cursor.execute('DELETE FROM timetables WHERE id = ?', (timetable_id,))
        
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def delete_all_timetables(department=None):
    """
    Delete all timetables, optionally filtered by department
    
    Args:
        department (str): If provided, only delete timetables from this department
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        if department:
            cursor.execute('DELETE FROM timetables WHERE department = ?', (department,))
        else:
            cursor.execute('DELETE FROM timetables')
        
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def update_timetable(timetable_id, schedule_data=None, department=None, semester=None, academic_year=None):
    """Update an existing timetable"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        updates = []
        params = []
        
        if schedule_data:
            updates.append("schedule_data = ?")
            params.append(json.dumps(schedule_data))
        
        if department:
            updates.append("department = ?")
            params.append(department)
        
        if semester:
            updates.append("semester = ?")
            params.append(semester)
        
        if academic_year:
            updates.append("academic_year = ?")
            params.append(academic_year)
        
        updates.append("updated_at = CURRENT_TIMESTAMP")
        
        if updates:
            params.append(timetable_id)
            query = f"UPDATE timetables SET {', '.join(updates)} WHERE id = ?"
            cursor.execute(query, params)
            conn.commit()
            return True
        
        return False
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def create_teacher(name, username, password_hash, email=None, department="CSE"):
    """Create a new teacher account"""
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute('''
            INSERT INTO teachers (name, username, password_hash, email, department)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, username, password_hash, email, department))

        conn.commit()
        return cursor.lastrowid
    except sqlite3.IntegrityError:
        # Username already exists
        return None
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def get_teacher_by_username(username):
    """Retrieve teacher by username"""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT * FROM teachers WHERE username = ? AND is_active = 1
    ''', (username,))

    row = cursor.fetchone()
    conn.close()

    return dict(row) if row else None

def get_teacher_by_id(teacher_id):
    """Retrieve teacher by ID"""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT id, name, username, email, department, password_hash, created_at
        FROM teachers WHERE id = ? AND is_active = 1
    ''', (teacher_id,))

    row = cursor.fetchone()
    conn.close()

    return dict(row) if row else None

def get_all_teachers():
    """Retrieve all active teachers"""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT id, name, username, email, department, created_at
        FROM teachers WHERE is_active = 1
        ORDER BY name
    ''')

    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]

def update_teacher_password(teacher_id, new_password_hash):
    """
    Update teacher's password
    
    Args:
        teacher_id (int): Teacher ID
        new_password_hash (str): New hashed password
    
    Returns:
        bool: True if successful, False otherwise
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute('''
            UPDATE teachers 
            SET password_hash = ?
            WHERE id = ? AND is_active = 1
        ''', (new_password_hash, teacher_id))

        conn.commit()
        success = cursor.rowcount > 0
        conn.close()
        return success
    except Exception as e:
        conn.rollback()
        conn.close()
        print(f"Error updating password: {e}")
        return False

# Initialize database on import
if __name__ == '__main__':
    init_db()
    print("Database setup complete!")
