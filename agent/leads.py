from flask import request, jsonify

from dbmodels.create import Customer, User
from dbmodels.create import Visit  # Import Visit model


def leads():
    if request.method == 'GET':
        """
        Render the leads page.
        """
        # Get all user_ids from Customer and Visit tables
        customer_user_ids = {c.user_id for c in Customer.query.with_entities(Customer.user_id).all()}
        visit_customer_ids = {v.customer_id for v in Visit.query.with_entities(Visit.customer_id).all()}
        all_user_ids = customer_user_ids.union(visit_customer_ids)

        # Query all users whose u_id is in all_user_ids and role is 'customer'
        users = User.query.filter(User.role == 'customer', User.u_id.in_(all_user_ids)).all()

        result = []
        for user in users:
            customer = Customer.query.filter_by(user_id=user.u_id).first()
            visit = Visit.query.filter_by(customer_id=user.u_id).order_by(Visit.visit_date.desc()).first()
            result.append({
                'id': user.id,
                'name': user.first_name + ' ' + user.last_name,
                'mobile': user.mobile,
                'status': customer.booking_status if customer else 'New user',
                'address': user.address if user.address else 'NA',
                'project': customer.interested_project if customer and customer.interested_project else 'None',
                'plot': customer.interested_plot if customer and customer.interested_plot else 'None',
                'site_visit': (
                    visit.visit_date.strftime('%Y-%m-%d') if visit and visit.visit_date else None
                ),
                'u_id': user.u_id if user.u_id else None,
            })
        return jsonify(result)
    if request.method == 'POST':
        data = request.get_json()
        # Process the lead data here
        # For example, you might save it to a database or perform some action
        print(data)
        return {'status': 'success', 'message': 'Lead processed successfully'}