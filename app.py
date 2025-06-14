import os

import jinja2
from flask import Flask, render_template, send_from_directory, jsonify, request, redirect, url_for, session
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

from admin.admin import admin
from agent.agent import agent
from customer.customer import customer
from dbmodels.create import User, Customer, db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'pdf'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db.init_app(app)
app.register_blueprint(admin)
app.register_blueprint(agent)
app.register_blueprint(customer)
print("Starting Flask server...")


def allowed_file(filename):
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


@app.route('/users.json')
@login_required
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


# TODO: move this to a separate module for user management
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Parse JSON fields from the 'data' blob
        if request.content_type.startswith('application/json'):
            # Handle pure JSON
            json_data = request.get_json()
            print('JSON:', json_data)
        import json
        json_blob = request.files.get('data')
        print(json_blob)
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

        # Validate passwords match
        if password != confirm_password:
            return 'Passwords do not match', 400

        # Handle file uploads
        aadhaar_file = request.files.get('aadhaar_file')
        pan_file = request.files.get('pan_file')
        if not (aadhaar_file and allowed_file(aadhaar_file.filename)):
            return 'Invalid Aadhaar file', 400
        if not (pan_file and allowed_file(pan_file.filename)):
            return 'Invalid PAN file', 400

        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        aadhaar_filename = secure_filename(aadhaar_file.filename)
        pan_filename = secure_filename(pan_file.filename)
        aadhaar_path = os.path.join(app.config['UPLOAD_FOLDER'], aadhaar_filename)
        pan_path = os.path.join(app.config['UPLOAD_FOLDER'], pan_filename)
        aadhaar_file.save(aadhaar_path)
        pan_file.save(pan_path)

        hashed_password = generate_password_hash(password)

        # Create user and customer as before...
        # (rest of your code unchanged)

        return redirect(url_for('login'))
    return render_template('register-basic.html')


# TODO: Add CSRF protection (e.g., with Flask-WTF), server-side form validation, and robust error handling before deploying to production.# TODO: Add CSRF protection (e.g., with Flask-WTF), server-side form validation,
#  and robust error handling before deploying to production.
def login():
    if not request.is_json:
        return jsonify({'status': 'error', 'message': 'Content-Type must be application/json'}), 400
    data = request.get_json()
    print(data)
    email = data.get('email')
    password = data.get('password')
    print(email, password)
    user = User.query.filter_by(email=email).first()
    print('User:', user)
    print(True if user and check_password_hash(user.password, password) else False)
    print(check_password_hash(user.password, password))
    if user and check_password_hash(user.password, password):
        session['user_id'] = user.id
        session['role'] = getattr(user, 'role', 'user')
        print('Logged in as {}'.format(user.email))
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


@app.route('/logout')
@login_required
def logout():
    session.pop('user_id', None)
    session.pop('role', None)
    return jsonify({'status': 'ok', 'message': 'Logged out'})


@app.route('/test', methods=['GET', 'POST'])
@login_required
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
                    {'value': 'Flats_ng', 'text': 'Luxury Flats'}
                ],
                'panasapadu': [
                    {'value': 'plots_pns', 'text': 'Plots'}
                ]
            },
            'sub2Options': {
                'villas_ng': [
                    {'value': 'villa1', 'text': 'Villa 1-East facing', 'size': 3200},
                    {'value': 'villa2', 'text': 'Villa 2-West facing', 'size': 3400}
                ],
                'Flats_ng': [
                    {'value': 'flat1', 'text': 'Flat no 101-East facing', 'size': 1200},
                    {'value': 'flat2', 'text': 'Flat no 102-West facing', 'size': 1250}
                ],
                'plots_pns': [
                    {'value': 'plot1', 'text': 'Plot 1-East facing', 'size': 180},
                    {'value': 'plot2', 'text': 'Plot 2-West facing', 'size': 220}
                ]
            },
        }
        if key in sample_data:
            return jsonify({'status': 'ok', key: sample_data[key]})
        return jsonify({'status': 'ok', **sample_data})
    return render_template('login-basic.html')

if __name__ == '__main__':
    app.run(debug=True)
