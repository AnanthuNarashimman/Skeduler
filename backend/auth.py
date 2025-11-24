"""
Authentication utilities for teacher login system
"""
import bcrypt
from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from database import get_teacher_by_username, get_teacher_by_id


def hash_password(password):
    """Hash a password using bcrypt"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def check_password(password, password_hash):
    """Verify a password against its hash"""
    return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))


def authenticate_teacher(username, password):
    """
    Authenticate a teacher with username and password

    Returns:
        dict: Teacher data if authentication succeeds, None otherwise
    """
    teacher = get_teacher_by_username(username)

    if not teacher:
        return None

    if check_password(password, teacher['password_hash']):
        # Remove password hash from returned data
        teacher_data = {
            'id': teacher['id'],
            'name': teacher['name'],
            'username': teacher['username'],
            'email': teacher['email'],
            'department': teacher['department']
        }
        return teacher_data

    return None


def teacher_required(fn):
    """
    Decorator to protect routes requiring teacher authentication
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
            teacher_id = get_jwt_identity()

            # Verify teacher still exists and is active
            teacher = get_teacher_by_id(teacher_id)
            if not teacher:
                return jsonify({'error': 'Teacher not found or inactive'}), 401

            return fn(*args, **kwargs)
        except Exception as e:
            return jsonify({'error': 'Authentication required', 'message': str(e)}), 401

    return wrapper


def get_current_teacher():
    """
    Get the currently authenticated teacher's data

    Returns:
        dict: Teacher data or None
    """
    try:
        verify_jwt_in_request()
        teacher_id = get_jwt_identity()
        return get_teacher_by_id(teacher_id)
    except:
        return None
