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


@app.route('/users.json')
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
        print(request.get_json())
        # Get form fields
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        dob = request.form.get('dob')
        gender = request.form.get('gender')
        adhar = request.form.get('adhar')
        pan = request.form.get('pan')
        role = 'customer'  # or get from form if needed

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

        # Create user
        user = User(name=f"{first_name} {last_name}", email=email, password=hashed_password, role=role)
        db.session.add(user)
        db.session.commit()

        # Create customer entry (add fields as per your Customer model)
        customer = Customer(
            user_id=user.id,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=hashed_password,
            dob=dob,
            gender=gender,
            adhar=adhar,
            pan=pan,
            aadhaar_file=aadhaar_filename,
            pan_file=pan_filename
        )
        db.session.add(customer)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register-basic.html')

# TODO: Add CSRF protection (e.g., with Flask-WTF), server-side form validation, and robust error handling before deploying to production.# TODO: Add CSRF protection (e.g., with Flask-WTF), server-side form validation,
#  and robust error handling before deploying to production.
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['role'] = getattr(user, 'role', None)
            if user.role == 'admin':
                return redirect(url_for('admin.dashboard'))
            elif user.role == 'agent':
                return redirect(url_for('agent.agent_dashboard'))
            elif user.role == 'customer':
                return redirect(url_for('customer.customer_dashboard'))
            else:
                return 'Unknown role', 403
        else:
            return render_template('login-basic.html', error='Invalid credentials')
    return render_template('login-basic.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('role', None)
    return redirect(url_for('index'))

@app.route('/test', methods=['GET', 'POST'])
def test():
    if request.method == 'POST':
        print(request.get_json())
        return jsonify({'status': 'ok', 'message': 'Test successful'})
    return render_template('login-basic.html')

if __name__ == '__main__':
    app.run(debug=True)