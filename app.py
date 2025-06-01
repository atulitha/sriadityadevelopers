import jinja2
from flask import Flask, render_template, send_from_directory

from agent.agent import agent
from admin.admin import admin
from customer.customer import customer

app = Flask(__name__)
app.register_blueprint(admin)
app.register_blueprint(agent)
app.register_blueprint(customer)
print("Starting Flask server...")

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/<pagename>')
def admin(pagename):
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


if __name__ == '__main__':
    app.run(debug=True)