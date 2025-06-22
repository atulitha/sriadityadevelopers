from datetime import datetime, timedelta

from flask import Flask
from werkzeug.security import generate_password_hash

from dbmodels.create import (
    db, Customer, Agent, Project, Plot,
    booking, Visit, feedback, User
)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../../users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


def create_db():
    with app.app_context():
        db.create_all()
        print("Database tables created successfully.")


def init_db():
    with app.app_context():
        # Create Agents and Users
        agents = []
        agent_users = [
            {
                'email': 'john.doe@gmail.com',
                'password': 'Agent@123',
                'role': 'agent',
                'first_name': 'John',
                'middle_name': 'Robert',
                'last_name': 'Doe',
                'office': 'Mumbai',
                'age': 35,
                'Address': '123 Main St',
                'start_date': datetime(2022, 1, 1),
                'percentage': 10,
                'sales': 500000.0,
                'status': 'Full-time',
                'phone': '9876543210',
                'adhar': '123456789012',
                'pan': 'ABCDE1234F',
                'designation': 'Senior Agent',
                'agent_team': 'Team A'
            },
            {
                'email': 'jane.smith@gmail.com',
                'password': 'Agent@123',
                'role': 'agent',
                'first_name': 'Jane',
                'middle_name': 'Marie',
                'last_name': 'Smith',
                'office': 'Delhi',
                'age': 28,
                'Address': '456 Oak Ave',
                'start_date': datetime(2022, 6, 1),
                'percentage': 8,
                'sales': 300000.0,
                'status': 'Part-time',
                'phone': '9876543211',
                'adhar': '123456789013',
                'pan': 'FGHIJ5678K',
                'designation': 'Agent',
                'agent_team': 'Team B'
            },
            {
                'email': 'satish@gmail.com',
                'password': 'Director@123',
                'role': 'director',
                'first_name': 'Satish',
                'last_name': '',
                'office': 'Bangalore',
                'age': 50,
                'Address': '789 Elm St',
                'start_date': datetime(2020, 1, 1),
                'percentage': 15,
                'sales': 10000000.0,
                'status': 'Full-time',
                'phone': '9876543213',
                'adhar': '123456789016',
                'pan': 'LMNOP6789R',
                'designation': 'Director',
                'agent_team': 'Management',
            },
        ]
        for agent_info in agent_users:
            user = User(
                first_name=agent_info['first_name'],
                last_name=agent_info['last_name'],
                email=agent_info['email'],
                password=generate_password_hash(agent_info['password']),
                dob=agent_info.get('dob', datetime(1985, 1, 1)),
                gender=agent_info.get('gender', 'Male'),
                adhar=agent_info['adhar'],
                pan=agent_info['pan'],
                aadhaar_file=agent_info.get('aadhaar_file', None),
                pan_file=agent_info.get('pan_file', None),
                designation=agent_info['designation'],
                role=agent_info['role'],
                reference_agent=agent_info.get('reference_agent', None),
                agent_team=agent_info.get('agent_team', None)
            )
            db.session.add(user)
            db.session.commit()
            agent = Agent(
                user_id=user.id,
                first_name=agent_info['first_name'],
                last_name=agent_info['last_name'],
                office=agent_info['office'],
                age=agent_info['age'],
                Address=agent_info['Address'],
                start_date=agent_info['start_date'],
                percentage=agent_info['percentage'],
                sales=agent_info['sales'],
                status=agent_info['status'],
                email=agent_info['email'],
                phone=agent_info['phone'],
                adhar=agent_info['adhar'],
                pan=agent_info['pan'],
                password=user.password,
                role=agent_info['role']
            )
            agents.append(agent)
        db.session.add_all(agents)
        db.session.commit()

        # Create Customers and Users
        customers = []
        customer_users = [
            {
                'name': 'Mike Johnson',
                'email': 'mike.j@gmail.com',
                'password': 'Customer@123',
                'role': 'customer',
                'first_name': 'Mike',
                'middle_name': 'Thomas',
                'last_name': 'Johnson',
                'age': 45,
                'address': '789 Pine Rd',
                'phone': '9876543212',
                'adhar': '123456789014',
                'pan': 'KLMNO9012P',
                'interested_project': 'Green Valley',
                'interested_plot': 'A-123',
                'booking_status': 'interested',
            },
            {
                'name': 'Sarah Wilson',
                'email': 'sarah.w@gmail.com',
                'password': 'Customer@123',
                'role': 'customer',
                'first_name': 'Sarah',
                'middle_name': 'Elizabeth',
                'last_name': 'Wilson',
                'age': 32,
                'address': '321 Cedar Ln',
                'phone': '9876543213',
                'adhar': '123456789015',
                'pan': 'QRSTU3456V',
                'interested_project': 'Blue Heights',
                'interested_plot': 'B-456',
                'booking_status': 'booked',
            }
        ]
        for cust_info in customer_users:
            user = User(
                first_name=cust_info['first_name'],
                last_name=cust_info['last_name'],
                email=cust_info['email'],
                password=generate_password_hash(cust_info['password']),
                dob=cust_info.get('dob', datetime(1990, 1, 1)),  # Example default
                gender=cust_info.get('gender', 'Male'),
                adhar=cust_info['adhar'],
                pan=cust_info['pan'],
                aadhaar_file=cust_info.get('aadhaar_file', None),
                pan_file=cust_info.get('pan_file', None),
                designation=cust_info.get('designation', None),
                role=cust_info['role'],
                reference_agent=cust_info.get('reference_agent', None),
                agent_team=cust_info.get('agent_team', None)
            )
            db.session.add(user)
            db.session.commit()
            customer = Customer(
                user_id=user.id,
                first_name=cust_info['first_name'],
                middle_name=cust_info['middle_name'],
                last_name=cust_info['last_name'],
                age=cust_info['age'],
                address=cust_info['address'],
                email=cust_info['email'],
                phone=cust_info['phone'],
                adhar=cust_info['adhar'],
                pan=cust_info['pan'],
                interested_project=cust_info['interested_project'],
                interested_plot=cust_info['interested_plot'],
                booking_status=cust_info['booking_status'],
                password=user.password,
                role=cust_info['role']
            )
            customers.append(customer)
        db.session.add_all(customers)
        db.session.commit()

        # Create Projects
        projects = [
            Project(
                name='Green Valley',
                description='Luxury villa project',
                location='Mumbai Suburbs',
                start_date=datetime(2022, 1, 1),
                end_date=datetime(2024, 12, 31),
                status='ongoing',
                total_area=50000.0,
                developer='ABC Developers'
            ),
            Project(
                name='Blue Heights',
                description='Premium apartments',
                location='Delhi NCR',
                start_date=datetime(2022, 6, 1),
                end_date=datetime(2025, 5, 31),
                status='ongoing',
                total_area=75000.0,
                developer='XYZ Builders'
            )
        ]
        db.session.add_all(projects)
        db.session.commit()

        # Create Plots
        plots = [
            Plot(
                project_id=projects[0].id,
                plot_number='A-123',
                size=2500.0,
                price=5000000.0,
                status='available'
            ),
            Plot(
                project_id=projects[1].id,
                plot_number='B-456',
                size=3000.0,
                price=7500000.0,
                status='reserved'
            )
        ]
        db.session.add_all(plots)
        db.session.commit()

        # Create Bookings
        bookings = [
            booking(
                customer_id=customers[1].id,
                plot_id=plots[1].id,
                booking_date=datetime.now(),
                status='confirmed',
                amount=750000.0,
                payment_status='paid',
                payment_date=datetime.now(),
                agent_id=agents[0].id
            )
        ]
        db.session.add_all(bookings)
        db.session.commit()

        # Create Visits
        visits = [
            visit(
                customer_id=customers[0].id,
                plot_id=plots[0].id,
                agent_id=agents[0].id,
                visit_date=datetime.now() + timedelta(days=7),
                purpose='Site inspection',
                feedback='Customer showed interest',
                status='scheduled'
            )
        ]
        db.session.add_all(visits)
        db.session.commit()

        # Create Feedbacks
        feedbacks = [
            feedback(
                customer_id=customers[1].id,
                comments='Excellent service and communication',
                rating=5,
                status='new'
            )
        ]
        db.session.add_all(feedbacks)
        db.session.commit()


if __name__ == '__main__':
    create_db()
    init_db()
    print("Database initialized successfully with mock data!")