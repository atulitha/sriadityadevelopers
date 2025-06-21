from flask import jsonify, request, session
from werkzeug.security import generate_password_hash

from lib import allowed_image, allowed_file
from dbmodels.create import db, User
from lib import validate_agent_data


def register_agent():
    # if 'user_id' not in session or session.get('role') != 'admin':
    #     return jsonify({'status': 'error', 'message': 'Authentication required'}), 401

    if request.method == 'POST':
        data = request.get_json()
        print(data)
        # Validate the registration data
        validation_result = validate_agent_data(data)
        if validation_result['status'] == 'error':
            return jsonify(validation_result), 400

        try:
            # Create new agent user
            hashed_password = generate_password_hash(data['password'])

            agent = User(
                name=f"{data['firstName']} {data['lastName']}",
                email=data['email'],
                password=hashed_password,
                dob=data['dob'],
                gender=data['gender'],
                designation=data['designation'],
                reference_agent=data['referenceAgent'],
                agent_team=data['agentTeam'],
                adhar=data['aadhaar'],
                pan=data['pan'],
                role='agent'
            )

            db.session.add(agent)
            db.session.commit()

            return jsonify({
                'status': 'ok',
                'message': 'Agent registered successfully',
                'agent_id': agent.id
            })

        except Exception as e:
            db.session.rollback()
            print(f"Error registering agent: {e}")
            return jsonify({
                'status': 'error',
                'message': 'Failed to register agent'
            }), 500

    # GET request returns form data structure
    return jsonify({
        'status': 'ok',
        'form_fields': {
            'firstName': '',
            'lastName': '',
            'email': '',
            'password': '',
            'confirmPassword': '',
            'dob': '',
            'gender': ['male', 'female', 'other'],
            'designation': '',
            'referenceAgent': '',
            'agentTeam': '',
            'aadhaar': '',
            'pan': ''
        }
    })