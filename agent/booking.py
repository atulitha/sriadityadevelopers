from datetime import datetime

from flask import request, jsonify, session

from dbmodels.create import User, Visit  # Assuming Visit is your visits table model


def book_visit():
    if request.method == 'POST':
        data = request.get_json()
        mobile = data.get('mobile_number')
        visit_date = data.get('visitDate')
        purpose = data.get('purpose')
        feedback = data.get('feedback')
        status = data.get('status', 'scheduled')
        plot_id = data.get('plot_id')
        created_date = datetime.now()

        user = User.query.filter_by(mobile=mobile).first()
        if not user:
            return jsonify({'status': 'error', 'message': 'Mobile not found'}), 404

        customer_id = user.id
        agent_id = session.get('user_id')

        if not all([customer_id, plot_id, agent_id, visit_date, purpose]):
            return jsonify({'status': 'error', 'message': 'Missing required fields'}), 400

        visit = Visit(
            customer_id=customer_id,
            plot_id=plot_id,
            agent_id=agent_id,
            visit_date=visit_date,
            purpose=purpose,
            feedback=feedback,
            status=status,
            created_date=created_date,
        )
        visit.save()  # Or db.session.add(visit); db.session.commit() depending on your ORM

        return jsonify({'status': 'success', 'message': 'Site visit booked successfully'})
    return None