from datetime import datetime

from flask import jsonify, request
from werkzeug.security import generate_password_hash

from dbmodels.create import db, User
from lib import validate_agent_data


def register_agent():
    # if 'user_id' not in session or session.get('role') != 'admin':
    #     return jsonify({'status': 'error', 'message': 'Authentication required'}), 401

    if request.method == 'GET':
        try:
            key = request.args.get('key')
            # Handle the key and return appropriate data
            # print(f"GET key: {key}")
            # Example: return designation list if key == 'Designation'
            if key == 'Designation':
                designations = db.session.query(User.designation).distinct().all()
                unique_designations = [d[0] for d in designations if d[0] is not None]
                unique_designations.sort()
                data = []
                for designation in unique_designations:
                    data.append({'id': designation, 'name': designation})
                # print(data)
                return jsonify({'status': 'ok', 'Designation': data})
            if key == 'teams':
                teams = db.session.query(User.agent_team).distinct().all()
                unique_teams = [t[0] for t in teams if t[0] is not None]
                unique_teams.remove(('Management'))
                unique_teams.sort()
                data = []
                for team in unique_teams:
                    data.append({'id': team, 'name': team})
                # print(data)
                return jsonify({'status': 'ok', 'teams': data})
            if key == 'agents':
                agents = db.session.query(User.id, User.first_name, User.last_name).filter_by(role='agent').all()
                data = [{'id': agent.id, 'name': f"{agent.first_name} {agent.last_name}"} for agent in agents]
                # print(data)
                return jsonify({'status': 'ok', 'name': data})
            if key == 'directors':
                directors = db.session.query(User.id, User.first_name, User.last_name).filter_by(role='director').all()
                data = [{'id': director.id, 'name': f"{director.first_name} {director.last_name}"} for director in
                        directors]
                # print(data)
                return jsonify({'status': 'ok', 'directors': data})
            else:
                return jsonify({'status': 'error', 'message': 'Invalid key provided'}), 400


        except Exception as e:
            # print(f"Error processing GET request: {e}")
            return jsonify({'status': 'error', 'message': 'Invalid request'}), 400

    if request.method == 'POST':
        data = request.get_json()
        # print(data)
        # Validate the registration data
        validation_result = validate_agent_data(data)
        if validation_result['status'] == 'error':
            return jsonify(validation_result), 400

        try:
            # Create new agent user
            hashed_password = generate_password_hash(data['password'])

            agent = User(
                first_name=data['firstName'],
                last_name=data['lastName'],
                email=data['email'],
                password=hashed_password,
                dob=datetime.strptime(data['dob'], '%Y-%m-%d').date(),
                gender=data['gender'],
                designation=data['designation'],
                reference_agent=data['referenceAgent'],
                agent_team=data['agentTeam'],
                adhar=data['aadhaar'],
                pan=data['pan'],
                role='agent',
                aadhaar_file=data.get('aadhaarFile', None),
                pan_file=data.get('panFile', None),
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
            # print(f"Error registering agent: {e}")
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