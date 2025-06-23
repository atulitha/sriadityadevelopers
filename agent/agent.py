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


@agent.route('/users', methods=['GET'])
def get_all_users():
    """
    Get all users as JSON.
    """
    users = User.query.all()
    return jsonify([
        {
            'id': user.id,
            'email': user.email,
            'name': user.name
        } for user in users
    ])


@agent.route('/book-site-visit.html', methods=['GET'])
def book_site_visit():
    """
    Book a site visit.

    This page allows the agent to book a site visit.
    """
    return render_template('book-visit.html')


# If booking.book_site_visit is a view function, register it as a route like this:
agent.add_url_rule('/book-visit', view_func=booking.book_visit, methods=['GET', 'POST'])
agent.add_url_rule('/dashboad2', view_func=booking.book_visit, methods=['GET', 'POST'])


@agent.route('/plotdata-tables1.html', methods=['GET'])
def plotdata_tables():
    """
    Book a site visit.

    This page allows the agent to book a site visit.
    """
    return render_template('plotdata-tables1.html')


@agent.route('/userdata-tables.html', methods=['GET'])
def userdata_tables():
    """
    Book a site visit.

    This page allows the agent to book a site visit.
    """
    return render_template('userdata-tables.html')


@agent.route('/<pagename>')
def serve_page(pagename):  # Changed from 'admin' to 'serve_page'
    return render_template(pagename)