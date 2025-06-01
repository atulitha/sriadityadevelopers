# blueprints/agent.py
from flask import Blueprint, render_template, request, jsonify, send_from_directory

from dbmodels.create import User

agent = Blueprint('agent', __name__, url_prefix='/agent',
                  template_folder='./', static_folder='static')


@agent.route('/')
def agent_index():
    """
    Agent index page.

    This is the main page for the agent. It renders ``index.html``.
    """
    return render_template('index.html')


@agent.route('/users')
def list_users():
    # Sample data - in real app, this would come from a database
    users = [
        {'id': 1, 'name': 'agent User', 'email': 'agent@example.com'},
        {'id': 2, 'name': 'Regular User', 'email': 'user@example.com'}
    ]
    return render_template('users.html', users=users)

@agent.route('/users.json')
def list_users_json():
    users = User.query.all()
    return jsonify({
        'status': 'ok',
        'data': [{
            'id': user.id,
            'first_name': user.first_name,
            'middle_name': user.middle_name,
            'last_name': user.last_name,
            'name': f"{user.first_name} {user.middle_name or ''} {user.last_name}",
            'position': user.position,
            'office': user.office,
            'age': user.age,
            'address': user.Address,
            'start_date': user.start_date.strftime('%Y/%m/%d') if user.start_date else None,
            'percentage': user.percentage,
            'sales': user.sales,
            'status': user.status,
            'email': user.email,
            'phone': user.phone,
            'adhar': user.adhar,
            'pan': user.pan,
            'created_at': user.created_at.strftime('%Y-%m-%d %H:%M:%S') if user.created_at else None,
            'updated_at': user.updated_at.strftime('%Y-%m-%d %H:%M:%S') if user.updated_at else None
        } for user in users]
    })

@agent.route('/users_api_format')
def users_api_format():
    """
    :return:
    """
    return render_template('user_api.html')


@agent.route('/settings', methods=['GET', 'POST'])
def settings():
    if request.method == 'POST':
        # Handle settings update
        return jsonify({'status': 'success'})
    return render_template('settings.html')


@agent.route('/<path:resource>')
def serveStaticResource(resource):
    return send_from_directory('static/', resource)