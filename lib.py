import re
from collections import defaultdict
from datetime import time
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

    # Check if email already exists
    if User.query.filter_by(email=data['email']).first():
        return {'status': 'error', 'message': 'Email already registered'}

    return {'status': 'ok'}


def rate_limiter():
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
        # Rate limiting
        if not rate_limiter():
            return jsonify({'status': 'error', 'message': 'Too many requests'}), 429
        # Require authentication
        if 'user_id' not in session:
            return jsonify({'status': 'error', 'message': 'Authentication required'}), 401
        return f(*args, **kwargs)

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