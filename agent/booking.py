from datetime import datetime

from flask import request, jsonify, session

from dbmodels.create import User, Visit, db  # Assuming Visit is your visits table model


def book_visit():
    if request.method == 'GET':
        """
        Render the booking page for site visits.
        """
        return jsonify({'visits': []})

    if request.method == 'POST':
        data = request.get_json()
        mobile = data.get('mobile_number')
        visit_date_str = data.get('visitDate')
        purpose = data.get('purpose')
        feedback = data.get('feedback')
        status = data.get('status', 'scheduled')
        plot_id = data.get('plotNumber')
        created_date = datetime.now()
        print(data)

        user = User.query.filter_by(mobile=mobile).first()
        if not user:
            return jsonify({'status': 'error', 'message': 'Mobile not found'}), 404

        visit = Visit.query.filter_by(customer_id=user.id, plot_id=plot_id).first()
        if visit:
            return jsonify({'status': 'error', 'message': 'Visit already exists for this customer and plot'}), 400

        customer_id = user.id
        agent_id = session.get('user_id')
        print(session.get('user_id'))
        print(session.get('role'))

        # Convert visit_date string to date object
        visit_date = datetime.strptime(visit_date_str, '%Y-%m-%d').date() if visit_date_str else None

        visit = Visit(
            customer_id=customer_id,
            plot_id=plot_id,
            agent_id=agent_id,
            visit_date=visit_date,
            purpose=purpose,
            feedback=feedback,
            status=status,
            created_at=created_date,
        )
        db.session.add(visit)
        db.session.commit()

        return jsonify({'status': 'success', 'message': 'Site visit booked successfully'})
    return None