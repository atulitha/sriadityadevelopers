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
                unique_designations.remove("Director")
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
        try:
            data = request.form.to_dict()
            # Add file data if present
            if 'aadhaarFile' in request.files:
                print('aadhaarFile')
                data['aadhaarFile'] = request.files['aadhaarFile']
                data['aadhaarFile'].save('static/uploads/')
            if 'panFile' in request.files:
                print('panFile')
                data['panFile'] = request.files['panFile']

            validation_result = validate_agent_data(data)
            if validation_result['status'] == 'error':
                return jsonify(validation_result), 400
            print(data)
            for x in request.files:
                print(x, request.files[x])
            aadhaar_file = request.files['aadhaar_file']
            aadhaar_file_bytes = aadhaar_file.read()
            pan_file = request.files['pan_file']
            pan_file_bytes = pan_file.read()
            photo = request.files['photo_file']
            photo_file_bytes = photo.read()
            if not aadhaar_file_bytes or not pan_file_bytes or not photo_file_bytes:
                return jsonify({
                    'status': 'error',
                    'message': 'Aadhaar, PAN, and Photo files are required'
                }), 400
            MAX_FILE_SIZE = 2 * 1024 * 1024  # 2 MB in bytes

            if (len(aadhaar_file_bytes) > MAX_FILE_SIZE or
                len(pan_file_bytes) > MAX_FILE_SIZE or
                len(photo_file_bytes) > MAX_FILE_SIZE):
                return jsonify({
                    'status': 'error',
                    'message': 'Aadhaar, PAN, and Photo files must be less than 2 MB each'
                }), 400

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
                aadhaar_file=aadhaar_file_bytes,
                pan_file=pan_file_bytes,
                photo=photo_file_bytes,
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