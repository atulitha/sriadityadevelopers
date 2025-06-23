import re
from collections import defaultdict
from functools import wraps

from flask import request, jsonify, session

from dbmodels.create import User

# --- Security: Simple Rate Limiting (per IP, per endpoint) ---
RATE_LIMIT = 100  # requests
RATE_PERIOD = 60  # seconds
rate_limits = defaultdict(list)
ALLOWED_EXTENSIONS = {'pdf'}


def validate_agent_data(data):
    required_fields = [
        'firstName', 'lastName', 'email', 'password', 'confirmPassword',
        'dob', 'gender', 'designation', 'referenceAgent', 'agentTeam',
        'aadhaar', 'pan'
    ]

    # Check required fields
    for field in required_fields:
        if field not in data:
            return {'status': 'error', 'message': f'Missing field: {field}'}

    # Password validation
    if data['password'] != data['confirmPassword']:
        return {'status': 'error', 'message': 'Passwords do not match'}
    if len(data['password']) < 8:
        return {'status': 'error', 'message': 'Password must be at least 8 characters'}

    # Email validation
    if not re.match(r'^[^@]+@[^@]+\.[^@]+$', data['email']):
        return {'status': 'error', 'message': 'Invalid email format'}

    # Check if reference agent format is valid
    errors = ""

    if data['referenceAgent'] and not User.query.filter_by(u_id=data['referenceAgent']).first():
        errors += "Reference agent does not exist.\n"

    if User.query.filter_by(email=data['email']).first():
        errors += "Email already registered.\n"

    if errors:
        return {'status': 'error', 'message': errors.strip()}

    return {'status': 'ok'}


def validate_customer_data(data):
    required_fields = [
        'first_name', 'last_name', 'email', 'phone', 'password', 'confirm_password',
        'dob', 'gender', 'address'
    ]
    # Check required fields
    for field in required_fields:
        if not data.get(field):
            return {'status': 'error', 'message': f'Missing field: {field}'}

    # Password validation
    if data['password'] != data['confirm_password']:
        return {'status': 'error', 'message': 'Passwords do not match'}
    if len(data['password']) < 8:
        return {'status': 'error', 'message': 'Password must be at least 8 characters'}

    # Email validation
    if not re.match(r'^[^@]+@[^@]+\.[^@]+$', data['email']):
        return {'status': 'error', 'message': 'Invalid email format'}

    # Phone validation
    if not re.match(r'^\d{10}$', data['phone']):
        return {'status': 'error', 'message': 'Phone number must be exactly 10 digits'}

    # Email uniqueness
    if User.query.filter_by(email=data['email']).first():
        return {'status': 'error', 'message': 'Email already registered'}

    # Phone uniqueness (use 'mobile' field in User)
    if User.query.filter_by(mobile=data['phone']).first():
        return {'status': 'error', 'message': 'Phone number already registered'}

    return {'status': 'ok'}


def rate_limiter():
    import time
    ip = request.remote_addr
    endpoint = request.endpoint
    now = time.time()
    window = [t for t in rate_limits[(ip, endpoint)] if now - t < RATE_PERIOD]
    window.append(now)
    rate_limits[(ip, endpoint)] = window
    if len(window) > RATE_LIMIT:
        return False
    return True


def api_security(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            if not rate_limiter():
                return jsonify({'status': 'error', 'message': 'Too many requests'}), 429
            if 'user_id' not in session:
                return jsonify({'status': 'error', 'message': 'Authentication required'}), 401
            return f(*args, **kwargs)
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)}), 500

    return decorated


def allowed_file(filename):
    # Sanitize filename
    if not filename or '/' in filename or '\\' in filename:
        return False
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def allowed_image(filename):
    ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    if not filename or '/' in filename or '\\' in filename:
        return False
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS
    pass


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'status': 'error', 'message': 'Authentication required'}), 401
        return f(*args, **kwargs)

    return decorated_function