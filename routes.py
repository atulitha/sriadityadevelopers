def register():
    import json
    json_blob = request.files.get('data')
    if not json_blob:
        return 'Missing form data', 400
    json_fields = json.load(json_blob)

    # Extract fields from JSON
    first_name = json_fields.get('first_name')
    last_name = json_fields.get('last_name')
    email = json_fields.get('email')
    password = json_fields.get('password')
    confirm_password = json_fields.get('confirm_password')
    dob = json_fields.get('dob')
    gender = json_fields.get('gender')
    adhar = json_fields.get('adhar')
    pan = json_fields.get('pan')
    role = 'customer'

    if password != confirm_password:
        return 'Passwords do not match', 400

    aadhaar_file = request.files.get('aadhaar_file')
    pan_file = request.files.get('pan_file')
    photo_file = request.files.get('photo')
    if not (aadhaar_file and allowed_file(aadhaar_file.filename)):
        return 'Invalid Aadhaar file', 400
    if not (pan_file and allowed_file(pan_file.filename)):
        return 'Invalid PAN file', 400
    if not (photo_file and allowed_image(photo_file.filename)):
        return 'Invalid photo file', 400

    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    aadhaar_filename = secure_filename(aadhaar_file.filename)
    pan_filename = secure_filename(pan_file.filename)
    photo_filename = secure_filename(photo_file.filename)
    aadhaar_path = os.path.join(app.config['UPLOAD_FOLDER'], aadhaar_filename)
    pan_path = os.path.join(app.config['UPLOAD_FOLDER'], pan_filename)
    photo_path = os.path.join(app.config['UPLOAD_FOLDER'], photo_filename)
    aadhaar_file.save(aadhaar_path)
    pan_file.save(pan_path)
    photo_file.save(photo_path)

    hashed_password = generate_password_hash(password)

    if not email or '@' not in email or len(email) > 255:
        return 'Invalid email', 400
    if not password or len(password) < 8:
        return 'Password too short', 400
    if User.query.filter_by(email=email).first():
        return 'Email already registered', 400

    user = User(
        name=f"{first_name} {last_name}",
        email=email,
        password=hashed_password,
        dob=dob,
        gender=gender,
        adhar=adhar,
        pan=pan,
        aadhaar_file=aadhaar_filename,
        pan_file=pan_filename,
        photo_file=photo_filename,  # Add this field to your User model
        role=role
    )
    db.session.add(user)
    db.session.commit()

    return jsonify({'status': 'ok', 'message': 'User registered'})