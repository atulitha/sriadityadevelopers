def register_agent():
    if 'user_id' not in session or session.get('role') != 'admin':
        return jsonify({'status': 'error', 'message': 'Authentication required'}), 401
    return render_template('register-agent.html')