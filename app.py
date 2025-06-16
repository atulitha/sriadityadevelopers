import os
from functools import wraps
import time
from collections import defaultdict

import jinja2
from flask import Flask, render_template, send_from_directory, jsonify, request, redirect, url_for, session, abort
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

from admin.admin import admin
from agent.agent import agent
from customer.customer import customer
from dbmodels.create import User, db

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-very-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'pdf'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# --- Security: Session cookie settings ---
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['SESSION_COOKIE_SECURE'] = True  # Set to True in production with HTTPS

# --- Security: Simple Rate Limiting (per IP, per endpoint) ---
RATE_LIMIT = 100  # requests
RATE_PERIOD = 60  # seconds
rate_limits = defaultdict(list)

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

db.init_app(app)
app.register_blueprint(admin)
app.register_blueprint(agent)
app.register_blueprint(customer)
print("Starting Flask server...")


def allowed_file(filename):
    # Sanitize filename
    if not filename or '/' in filename or '\\' in filename:
        return False
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return render_template('login-basic.html')


@app.route('/<pagename>')
def serve_page(pagename):  # Changed from 'admin' to 'serve_page'
    return render_template(pagename)


@app.route('/<path:resource>')
def serveStaticResource(resource):
    return send_from_directory('static/', resource)


@app.errorhandler(jinja2.exceptions.TemplateNotFound)
def template_not_found(e):
    return not_found(e)


@app.errorhandler(404)
def not_found(e):
    return '<strong>Page Not Found!</strong>', 404


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'status': 'error', 'message': 'Authentication required'}), 401
        return f(*args, **kwargs)

    return decorated_function


@app.route('/users.json', methods=['GET'])
@api_security
def list_users_json():
    users = User.query.all()
    return jsonify({
        'status': 'ok',
        'data': [{
            'id': user.id,
            'email': user.email,
            'name': f"{user.name}",
        } for user in users]
    })


@app.route('/register', methods=['POST'])
def register():
    import json
    json_blob = request.files.get('data')
    if not json_blob:
        return 'Missing form data', 400
    json_fields = json.load(json_blob)

    # Extract fields from JSON
    first_name = json_fields.get('first_name')
    last_name = json_fields.get('last_name')
    email = json_fields.get('email')
    password = json_fields.get('password')
    confirm_password = json_fields.get('confirm_password')
    dob = json_fields.get('dob')
    gender = json_fields.get('gender')
    adhar = json_fields.get('adhar')
    pan = json_fields.get('pan')
    role = 'customer'

    if password != confirm_password:
        return 'Passwords do not match', 400

    aadhaar_file = request.files.get('aadhaar_file')
    pan_file = request.files.get('pan_file')
    photo_file = request.files.get('photo')
    if not (aadhaar_file and allowed_file(aadhaar_file.filename)):
        return 'Invalid Aadhaar file', 400
    if not (pan_file and allowed_file(pan_file.filename)):
        return 'Invalid PAN file', 400
    if not (photo_file and allowed_image(photo_file.filename)):
        return 'Invalid photo file', 400

    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    aadhaar_filename = secure_filename(aadhaar_file.filename)
    pan_filename = secure_filename(pan_file.filename)
    photo_filename = secure_filename(photo_file.filename)
    aadhaar_path = os.path.join(app.config['UPLOAD_FOLDER'], aadhaar_filename)
    pan_path = os.path.join(app.config['UPLOAD_FOLDER'], pan_filename)
    photo_path = os.path.join(app.config['UPLOAD_FOLDER'], photo_filename)
    aadhaar_file.save(aadhaar_path)
    pan_file.save(pan_path)
    photo_file.save(photo_path)

    hashed_password = generate_password_hash(password)

    if not email or '@' not in email or len(email) > 255:
        return 'Invalid email', 400
    if not password or len(password) < 8:
        return 'Password too short', 400
    if User.query.filter_by(email=email).first():
        return 'Email already registered', 400

    user = User(
        name=f"{first_name} {last_name}",
        email=email,
        password=hashed_password,
        dob=dob,
        gender=gender,
        adhar=adhar,
        pan=pan,
        aadhaar_file=aadhaar_filename,
        pan_file=pan_filename,
        photo_file=photo_filename,  # Add this field to your User model
        role=role
    )
    db.session.add(user)
    db.session.commit()

    return jsonify({'status': 'ok', 'message': 'User registered'})


@app.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({'status': 'error', 'message': 'Content-Type must be application/json'}), 400
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    # Validate input
    if not email or not password:
        return jsonify({'status': 'error', 'message': 'Missing credentials'}), 400
    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password, password):
        session['user_id'] = user.id
        session['role'] = getattr(user, 'role', 'user')
        return jsonify({
            'status': 'ok',
            'user': {
                'id': user.id,
                'email': user.email,
                'role': getattr(user, 'role', None),
                'name': user.name
            }
        })
    else:
        return jsonify({'status': 'error', 'message': 'Invalid username or password'}), 401


@app.route('/logout', methods=['POST'])
@api_security
def logout():
    session.pop('user_id', None)
    session.pop('role', None)
    return jsonify({'status': 'ok', 'message': 'Logged out'})

@app.route('/test', methods=['GET', 'POST'])
def test():
    if request.method == 'POST':
        if request.content_type.startswith('application/json'):
            # Handle pure JSON
            json_data = request.get_json()
            print('JSON:', json_data)
            return jsonify({'status': 'ok', 'type': 'json', 'data': json_data})
        elif request.content_type.startswith('multipart/form-data'):
            # Handle multipart with JSON blob and files
            import json
            json_blob = request.files.get('data')
            json_fields = json.load(json_blob) if json_blob else {}
            print('Form JSON:', json_fields)
            print('Files:', request.files)
            return jsonify({'status': 'ok', 'type': 'multipart', 'data': json_fields})
        else:
            return jsonify({'status': 'error', 'message': 'Unsupported Content-Type'}), 415
    if request.method == 'GET':
        key = request.args.get('key')
        sample_data = {
            'agents': [
                {'id': 1, 'name': 'Self Registration'},
                {'id': 2, 'name': 'Agent Jhon'},
                {'id': 3, 'name': 'Agent Smith'}
            ],
            'directors': [
                {'id': 1, 'name': 'Director Brown'},
                {'id': 2, 'name': 'Director White'}
            ],
            'teams': [
                {'id': 1, 'name': 'Team Alpha'},
                {'id': 2, 'name': 'Team Beta'}
            ],
            'Designation': [
                {'id': 1, 'name': 'Manager'},
                {'id': 2, 'name': 'Executive'}
            ],
            'sub1Options': {
                'nandagokulam': [
                    {'value': 'villas_ng', 'text': 'Luxury Villas'},
                    {'value': 'Flats_ng', 'text': 'Luxury Flats'},
                    {'value': 'plots_ng', 'text': 'Plots'}
                ],
                'panasapadu': [
                    {'value': 'villas_pns', 'text': 'Luxury Villas'},
                    {'value': 'Flats_pns', 'text': 'Luxury Flats'}
                ]
            },
            'sub2Options': {
                'villas_ng': [
                    {'value': 'villa1', 'text': 'Villa 1-East facing'},
                    {'value': 'villa2', 'text': 'Villa 2-West facing'}
                ],
                'Flats_ng': [
                    {'value': 'flat1', 'text': 'Flat no 101-East facing'},
                    {'value': 'flat2', 'text': 'Flat no 102-West facing'}
                ],
                'villas_pns': [
                    {'value': 'villa1', 'text': 'Villa 1-East facing'},
                    {'value': 'villa2', 'text': 'Villa 2-West facing'}
                ],
                'Flats_pns': [
                    {'value': 'flat1', 'text': 'Flat no 101-East facing'},
                    {'value': 'flat 2', 'text': 'Flat no 102-West facing'}
                ]
            },

        }
        if key in sample_data:
            return jsonify({'status': 'ok', key: sample_data[key]})
        return jsonify({'status': 'ok', **sample_data})
    return render_template('login-basic.html')


# --- Security: Hide error details in production ---
@app.errorhandler(Exception)
def handle_exception(e):
    # Only show details in debug mode
    if app.debug:
        return jsonify({'status': 'error', 'message': str(e)}), 500
    return jsonify({'status': 'error', 'message': 'Internal server error'}), 500


if __name__ == '__main__':
    app.run(debug=True)