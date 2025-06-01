# blueprints/admin.py
from flask import Blueprint, render_template, request, jsonify

admin = Blueprint('admin', __name__, url_prefix='/admin')


@admin.route('/')
def admin_index():
    return render_template('admin/index.html')


@admin.route('/users')
def list_users():
    # Sample data - in real app, this would come from a database
    users = [
        {'id': 1, 'name': 'Admin User', 'email': 'admin@example.com'},
        {'id': 2, 'name': 'Regular User', 'email': 'user@example.com'}
    ]
    return render_template('admin/users.html', users=users)


@admin.route('/settings', methods=['GET', 'POST'])
def settings():
    if request.method == 'POST':
        # Handle settings update
        return jsonify({'status': 'success'})
    return render_template('admin/settings.html')