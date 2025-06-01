# blueprints/agent.py
from flask import Blueprint, render_template, request, jsonify, send_from_directory

agent = Blueprint('agent', __name__, url_prefix='/agent')


@agent.route('/')
def agent_index():
    return render_template('index.html')


@agent.route('/users')
def list_users():
    # Sample data - in real app, this would come from a database
    users = [
        {'id': 1, 'name': 'agent User', 'email': 'agent@example.com'},
        {'id': 2, 'name': 'Regular User', 'email': 'user@example.com'}
    ]
    return render_template('users.html', users=users)


@agent.route('/settings', methods=['GET', 'POST'])
def settings():
    if request.method == 'POST':
        # Handle settings update
        return jsonify({'status': 'success'})
    return render_template('settings.html')


@agent.route('/<path:resource>')
def serveStaticResource(resource):
    return send_from_directory('static/', resource)