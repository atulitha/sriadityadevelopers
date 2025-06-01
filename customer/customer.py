# blueprints/customer.py
from flask import Blueprint, render_template, request, jsonify, send_from_directory

customer = Blueprint('customer', __name__, url_prefix='/customer')


@customer.route('/')
def customer_index():
    return render_template('index.html')


@customer.route('/users')
def list_users():
    # Sample data - in real app, this would come from a database
    users = [
        {'id': 1, 'name': 'customer User', 'email': 'customer@example.com'},
        {'id': 2, 'name': 'Regular User', 'email': 'user@example.com'}
    ]
    return render_template('users.html', users=users)


@customer.route('/settings', methods=['GET', 'POST'])
def settings():
    if request.method == 'POST':
        # Handle settings update
        return jsonify({'status': 'success'})
    return render_template('settings.html')


@customer.route('/<path:resource>')
def serveStaticResource(resource):
    return send_from_directory('static/', resource)