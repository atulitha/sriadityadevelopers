# blueprints/agent.py
from flask import Blueprint, render_template, request, jsonify, send_from_directory

from dbmodels.create import User

from . import booking
agent = Blueprint('agent', __name__, url_prefix='/agent',
                  template_folder='./', static_folder='static')


@agent.route('/')
def agent_index():
    """
    Agent index page.

    This is the main page for the agent. It renders ``index.html``.
    """
    return render_template('agent-dashboard.html')


@agent.route('/settings', methods=['GET', 'POST'])
def settings():
    if request.method == 'POST':
        # Handle settings update
        return jsonify({'status': 'success'})
    return render_template('settings.html')


@agent.route('/<path:resource>')
def serveStaticResource(resource):
    return send_from_directory('static/', resource)


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
            'email': user.email,
            'name': f"{user.name}",
        } for user in users]
    })


@agent.route('/users_api_format')
def users_api_format():
    """
    :return:
    """
    return render_template('user_api.html')


@agent.route('/book-site-visit.html', methods=['GET'])
def book_site_visit():
    """
    Book a site visit.

    This page allows the agent to book a site visit.
    """
    return render_template('book-visit.html')

# If booking.book_site_visit is a view function, register it as a route like this:
agent.add_url_rule('/book-visit', view_func=booking.book_visit, methods=['GET', 'POST'])