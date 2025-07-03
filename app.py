import jinja2
from flask import Flask, render_template, send_from_directory, jsonify, request, session
from werkzeug.security import check_password_hash

import views
from admin.admin import admin
from agent.agent import agent
from customer.customer import customer
from dbmodels.create import User, db
from flask_session import Session
from lib import api_security

app = Flask(__name__)
app.config['SECRET_KEY'] = 'adityadeveloper'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
UPLOAD_FOLDER = 'static/uploads'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# --- Flask-Session config for Filesystem (development) ---
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = './flask_session'  # Optional: custom session file dir
app.config['SESSION_PERMANENT'] = False

# If you want to use Memcached in production, use:
# from pymemcache.client.base import Client as MemcacheClient
# app.config['SESSION_TYPE'] = 'memcached'
# app.config['SESSION_MEMCACHED'] = MemcacheClient(('127.0.0.1', 11211))

# --- Security: Session cookie settings ---
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['SESSION_COOKIE_SECURE'] = False  # Set to True in production with HTTPS

Session(app)  # <-- Initialize Flask-Session

db.init_app(app)
app.register_blueprint(admin)
app.register_blueprint(agent)
app.register_blueprint(customer)
print("Starting Flask server...")


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
    user = User.query.filter_by(u_id=email.lower()).first()
    if user and check_password_hash(user.password, password):
        session['user_id'] = user.id
        session['role'] = getattr(user, 'role', 'user')
        return jsonify({'status': 'ok',
                        'user': {'id': user.id, 'email': user.email, 'role': getattr(user, 'role', None),
                                 'name': user.first_name + ' ' + user.last_name}}), 200
    else:
        print("Invalid login attempt for user:", data)
        return jsonify({'status': 'error', 'message': 'Invalid username or password'}), 401


@app.route("/get_name", methods=['GET'])
@api_security
def get_name():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'status': 'error', 'message': 'User not logged in'}), 401
    user = db.session.get(User, user_id)
    if not user:
        return jsonify({'status': 'error', 'message': 'User not found'}), 404
    return jsonify({'status': 'ok', 'name': f"{user.first_name} {user.last_name}"})


@app.route('/logout', methods=['GET'])
@api_security
def logout():
    session.pop('user_id', None)
    session.pop('role', None)
    print('User logged out')
    return jsonify({'status': 'ok', 'message': 'Logged out'})


@app.route('/test', methods=['GET', 'POST'])
def test():
    if request.method == 'POST':
        if request.content_type.startswith('application/json'):
            # Handle pure JSON
            json_data = request.get_json()
            print('JSON:', json_data)
            return jsonify({
                'status': 'error',
                'message': 'data received',
            }), 500
        elif request.content_type.startswith('multipart/form-data'):
            # Handle multipart with JSON blob and files
            import json
            json_blob = request.files.get('data')
            json_fields = json.load(json_blob) if json_blob else {}
            print('Files:', request.files)
            form = request.form.to_dict()
            print(form)
            return jsonify({
                'status': 'error',
                'message': 'recived data'
            }), 500
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
            'projectdetails1': {
                'project1': [
                    {'value': 'villas_ng', 'text': 'Luxury Villas'},
                    {'value': 'Flats_ng', 'text': 'Luxury Flats'},
                    {'value': 'plots_ng', 'text': 'Plots'}
                ],
                'project2': [
                    {'value': 'plots_pns', 'text': 'Plots'}
                ]
            },
            'projectdetails2': {
                'villas_ng': [
                    {'value': 'villa1', 'text': 'Villa 1-East facing', 'size': 2500},
                    {'value': 'villa2', 'text': 'Villa 2-West facing', 'size': 2600}
                ],
                'Flats_ng': [
                    {'value': 'flat1', 'text': 'Flat no 101-East facing', 'size': 1200},
                    {'value': 'flat2', 'text': 'Flat no 102-West facing', 'size': 1250}
                ],
                'plots_ng': [
                    {'value': 'plot1', 'text': 'Plot 1', 'size': 300},
                    {'value': 'plot2', 'text': 'Plot 2', 'size': 320}
                ],
                'plots_pns': [
                    {'value': 'plot1', 'text': 'Plot 1', 'size': 350},
                    {'value': 'plot2', 'text': 'Plot 2', 'size': 370}
                ]
            },
            'projects': [
                {"id": 'Aditya Enclave', "name": "Aditya Enclave"},
                {"id": "Aditya Heights", "name": "Aditya Heights"},
                {"id": "Aditya Meadows", "name": "Aditya Meadows"},
                {"id": "Aditya Greens", "name": "Aditya Greens"},
                {"id": "Aditya Pearl", "name": "Aditya Pearl"}
            ],
            "Designation": [
                {"id": "Agent", "name": "Agent"},
                {"id": "Director", "name": "Director"},
                {"id": "Manager", "name": "Manager"},
                {"id": "Senior Agent", "name": "Senior Agent"},
                {"id": "Team Lead", "name": "Team Lead"}
            ],
            "teams": [
                {"id": "Team A", "name": "Team A"},
                {"id": "Team Alpha", "name": "Team Alpha"},
                {"id": "Team B", "name": "Team B"},
                {"id": "Team Beta", "name": "Team Beta"},
                {"id": "Team C", "name": "Team C"},
                {"id": "Team D", "name": "Team D"},
                {"id": "Team Delta", "name": "Team Delta"},
                {"id": "Team Gamma", "name": "Team Gamma"}
            ],
            "name": [
                {"id": 9, "name": "Jane Smith"},
                {"id": 10, "name": "Raj Yadav"}
            ],
            "directors": [
                {"id": 1, "name": "Satish Kumar"},
                {"id": 2, "name": "Anita Sharma"}
            ],

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


app.add_url_rule('/register-agent', '/register_agent', view_func=views.register_agent, methods=['GET', 'POST'])
app.add_url_rule('/register-customer', '/register_customer', view_func=views.register_customer, methods=['GET', 'POST'])

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)