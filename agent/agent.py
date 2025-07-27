# blueprints/agent.py
from flask import Blueprint, render_template, send_from_directory

from lib import api_security
from . import booking
from . import leads

agent = Blueprint('agent', __name__, url_prefix='/agent',
                  template_folder='./', static_folder='static')


@agent.route('/')
# @api_security
def agent_index():
    """
    Agent index page.

    This is the main page for the agent. It renders ``index.html``.
    """
    return render_template('agent-dashboard.html')


@agent.route('/<path:resource>')
def serveStaticResource(resource):
    return send_from_directory('static/', resource)


@agent.route('/book-site-visit.html', methods=['GET'])
# @api_security
def book_site_visit():
    """
    Book a site visit.

    This page allows the agent to book a site visit.
    """
    return render_template('book-visit.html')


# If booking.book_site_visit is a view function, register it as a route like this:
agent.add_url_rule('/book-visit', view_func=booking.book_visit, methods=['GET', 'POST'])
agent.add_url_rule('/dashboad2', view_func=booking.book_visit, methods=['GET', 'POST'])
agent.add_url_rule('/leads', view_func=leads.leads, methods=['GET', 'POST'])


@agent.route('/plotdata-tables1.html', methods=['GET'])
# @api_security
def plotdata_tables():
    """
    Book a site visit.

    This page allows the agent to book a site visit.
    """
    return render_template('plotdata-tables1.html')


@agent.route('/<pagename>')
# @api_security
def serve_page(pagename):  # Changed from 'admin' to 'serve_page'
    return render_template(pagename)