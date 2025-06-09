import jinja2
from flask import Flask, render_template, send_from_directory, jsonify, request, redirect, url_for, session
from werkzeug.security import check_password_hash, generate_password_hash

from admin.admin import admin
from agent.agent import agent
from customer.customer import customer
from dbmodels.create import User, Customer, Agent, db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']  # 'customer', 'agent', or 'admin'
        hashed_password = generate_password_hash(password)
        # Create user
        user = User(name=name, email=email, password=hashed_password, role=role)
        db.session.add(user)
        db.session.commit()
        # Create role-specific entry
        if role == 'customer':
            customer = Customer(user_id=user.id, first_name=name, email=email, password=hashed_password)
            db.session.add(customer)
        elif role == 'agent':
            agent = Agent(user_id=user.id, first_name=name, email=email, password=hashed_password)
            db.session.add(agent)
        elif role == 'admin':
            from dbmodels.create import Admin
            admin = Admin(user_id=user.id)
            db.session.add(admin)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register-basic.html')


@app.route('/login', methods=['GET', 'POST'])
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


if __name__ == '__main__':
    app.run(debug=True)