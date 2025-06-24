from flask import request, jsonify

from dbmodels.create import Customer, User


def leads():
    if request.method == 'GET':
        """
        Render the leads page.
        """
        customers = Customer.query.all()
        user = User.query.filter_by(role='customer').first()
        return jsonify([
            {
                'id': user.id,
                'name': user.first_name+' ' + user.last_name,
                'mobile': user.phone,
                'email': customer.email,
                'status': customer.booking_status,
                'address': customer.address,
                'project': customer.interested_project if customer.interested_project else None,
                'plot': customer.interested_plot if customer.interested_plot else None,
                'site_visit': None,
            } for customer in customers
        ])
    if request.method == 'POST':
        data = request.get_json()
        # Process the lead data here
        # For example, you might save it to a database or perform some action
        print(data)
        return {'status': 'success', 'message': 'Lead processed successfully'}