from flask import request, jsonify

from dbmodels.create import Customer, User
from dbmodels.create import Visit  # Import Visit model


def leads():
    if request.method == 'GET':
        """
        Render the leads page.
        """
        users = User.query.filter_by(role='customer').all()
        return jsonify([
            {
                'id': user.id,
                'name': user.first_name + ' ' + user.last_name,
                'mobile': user.mobile,
                'status': customer.booking_status if customer else 'New user',
                'address': user.address if user.address else 'NA',
                'project': customer.interested_project if customer and customer.interested_project else 'None',
                'plot': customer.interested_plot if customer and customer.interested_plot else 'None',
                # Get site_visit from visits table by customer_id (not user_id)
                'site_visit': (
                    (visit.visit_date if visit else None)
                ),
                'u_id': user.u_id if user.u_id else None,
            }
            for user in users
            for customer in [Customer.query.filter_by(user_id=user.u_id).first()]
            for visit in [Visit.query.filter_by(customer_id=user.u_id).first()]
        ])
    if request.method == 'POST':
        data = request.get_json()
        # Process the lead data here
        # For example, you might save it to a database or perform some action
        print(data)
        return {'status': 'success', 'message': 'Lead processed successfully'}