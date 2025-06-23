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
            # 2 Directors
            {
                'email': 'director1@gmail.com',
                'password': 'Director@123',
                'role': 'director',
                'first_name': 'Satish',
                'middle_name': '',
                'last_name': 'Kumar',
                'office': 'Bangalore',
                'age': 50,
                'Address': '789 Elm St',
                'start_date': datetime(2020, 1, 1),
                'percentage': 15,
                'sales': 10000000.0,
                'status': 'Full-time',
                'phone': '9876543210',
                'adhar': '123456789010',
                'pan': 'DIRCT0001F',
                'designation': 'Director',
                'agent_team': 'Management',
            },
            {
                'email': 'director2@gmail.com',
                'password': 'Director@123',
                'role': 'director',
                'first_name': 'Anita',
                'middle_name': '',
                'last_name': 'Sharma',
                'office': 'Hyderabad',
                'age': 48,
                'Address': '123 Director Ave',
                'start_date': datetime(2021, 2, 1),
                'percentage': 15,
                'sales': 9500000.0,
                'status': 'Full-time',
                'phone': '9876543211',
                'adhar': '123456789011',
                'pan': 'DIRCT0002F',
                'designation': 'Director',
                'agent_team': 'Management',
            },
            # 2 Managers
            {
                'email': 'manager1@gmail.com',
                'password': 'Manager@123',
                'role': 'manager',
                'first_name': 'Ravi',
                'middle_name': '',
                'last_name': 'Verma',
                'office': 'Pune',
                'age': 40,
                'Address': '456 Manager Rd',
                'start_date': datetime(2021, 3, 1),
                'percentage': 12,
                'sales': 7000000.0,
                'status': 'Full-time',
                'phone': '9876543212',
                'adhar': '123456789012',
                'pan': 'MANGR0001F',
                'designation': 'Manager',
                'agent_team': 'Team Alpha',
            },
            {
                'email': 'manager2@gmail.com',
                'password': 'Manager@123',
                'role': 'manager',
                'first_name': 'Priya',
                'middle_name': '',
                'last_name': 'Singh',
                'office': 'Chennai',
                'age': 38,
                'Address': '789 Manager St',
                'start_date': datetime(2021, 4, 1),
                'percentage': 12,
                'sales': 6800000.0,
                'status': 'Full-time',
                'phone': '9876543213',
                'adhar': '123456789013',
                'pan': 'MANGR0002F',
                'designation': 'Manager',
                'agent_team': 'Team Beta',
            },
            # 2 Team Leads
            {
                'email': 'teamlead1@gmail.com',
                'password': 'TeamLead@123',
                'role': 'team lead',
                'first_name': 'Amit',
                'middle_name': '',
                'last_name': 'Patel',
                'office': 'Delhi',
                'age': 34,
                'Address': '321 Teamlead Ln',
                'start_date': datetime(2022, 1, 1),
                'percentage': 11,
                'sales': 4000000.0,
                'status': 'Full-time',
                'phone': '9876543214',
                'adhar': '123456789014',
                'pan': 'TMLAD0001F',
                'designation': 'Team Lead',
                'agent_team': 'Team Gamma',
            },
            {
                'email': 'teamlead2@gmail.com',
                'password': 'TeamLead@123',
                'role': 'team lead',
                'first_name': 'Sneha',
                'middle_name': '',
                'last_name': 'Gupta',
                'office': 'Kolkata',
                'age': 33,
                'Address': '654 Teamlead Ave',
                'start_date': datetime(2022, 2, 1),
                'percentage': 11,
                'sales': 3900000.0,
                'status': 'Full-time',
                'phone': '9876543215',
                'adhar': '123456789015',
                'pan': 'TMLAD0002F',
                'designation': 'Team Lead',
                'agent_team': 'Team Delta',
            },
            # 2 Senior Agents
            {
                'email': 'senioragent1@gmail.com',
                'password': 'SeniorAgent@123',
                'role': 'senior agent',
                'first_name': 'John',
                'middle_name': 'Robert',
                'last_name': 'Doe',
                'office': 'Mumbai',
                'age': 35,
                'Address': '123 Main St',
                'start_date': datetime(2022, 3, 1),
                'percentage': 10,
                'sales': 500000.0,
                'status': 'Full-time',
                'phone': '9876543216',
                'adhar': '123456789016',
                'pan': 'SNAGT0001F',
                'designation': 'Senior Agent',
                'agent_team': 'Team A'
            },
            {
                'email': 'senioragent2@gmail.com',
                'password': 'SeniorAgent@123',
                'role': 'senior agent',
                'first_name': 'Meena',
                'middle_name': 'R.',
                'last_name': 'Nair',
                'office': 'Ahmedabad',
                'age': 36,
                'Address': '456 Senior St',
                'start_date': datetime(2022, 4, 1),
                'percentage': 10,
                'sales': 480000.0,
                'status': 'Full-time',
                'phone': '9876543217',
                'adhar': '123456789017',
                'pan': 'SNAGT0002F',
                'designation': 'Senior Agent',
                'agent_team': 'Team B'
            },
            # 2 Agents
            {
                'email': 'agent1@gmail.com',
                'password': 'Agent@123',
                'role': 'agent',
                'first_name': 'Jane',
                'middle_name': 'Marie',
                'last_name': 'Smith',
                'office': 'Delhi',
                'age': 28,
                'Address': '456 Oak Ave',
                'start_date': datetime(2022, 5, 1),
                'percentage': 8,
                'sales': 300000.0,
                'status': 'Part-time',
                'phone': '9876543218',
                'adhar': '123456789018',
                'pan': 'AGENT0001F',
                'designation': 'Agent',
                'agent_team': 'Team C'
            },
            {
                'email': 'agent2@gmail.com',
                'password': 'Agent@123',
                'role': 'agent',
                'first_name': 'Raj',
                'middle_name': 'S.',
                'last_name': 'Yadav',
                'office': 'Lucknow',
                'age': 29,
                'Address': '789 Agent Rd',
                'start_date': datetime(2022, 6, 1),
                'percentage': 8,
                'sales': 290000.0,
                'status': 'Part-time',
                'phone': '9876543219',
                'adhar': '123456789019',
                'pan': 'AGENT0002F',
                'designation': 'Agent',
                'agent_team': 'Team D'
            },
        ]
        agent_counters = {'ag': 1, 'mg': 1, 'md': 1}
        u_id_map = {'ag': [], 'mg': [], 'md': []}
        for idx, agent_info in enumerate(agent_users):
            role = agent_info.get('role', 'agent').lower()
            if role in ['agent', 'team lead', 'senior agent']:
                u_id = f"ag-{agent_counters['ag']:06d}"
                agent_counters['ag'] += 1
                u_id_map['ag'].append(u_id)
            elif role == 'manager':
                u_id = f"mg-{agent_counters['mg']:06d}"
                agent_counters['mg'] += 1
                u_id_map['mg'].append(u_id)
            elif role == 'director':
                u_id = f"md-{agent_counters['md']:06d}"
                agent_counters['md'] += 1
                u_id_map['md'].append(u_id)
            else:
                u_id = f"ag-{idx+1:06d}"  # fallback

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
                reference_agent=None,
                agent_team=agent_info.get('agent_team', None),
                mobile=agent_info.get('phone', None),
                u_id=u_id
            )
            db.session.add(user)
            db.session.commit()
            agent = Agent(
                user_id=user.u_id,
                first_name=agent_info['first_name'],
                middle_name=agent_info.get('middle_name', ''),
                last_name=agent_info['last_name'],
                position=agent_info.get('designation', 'Agent'),
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
                'phone': '9876543220',
                'adhar': '123456789020',
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
                'phone': '9876543221',
                'adhar': '123456789021',
                'pan': 'QRSTU3456V',
                'interested_project': 'Blue Heights',
                'interested_plot': 'B-456',
                'booking_status': 'booked',
            },
            {
                'name': 'Ajay Kumar',
                'email': 'ajay.k@gmail.com',
                'password': 'Customer@123',
                'role': 'customer',
                'first_name': 'Ajay',
                'middle_name': '',
                'last_name': 'Kumar',
                'age': 38,
                'address': '111 Maple St',
                'phone': '9876543222',
                'adhar': '123456789022',
                'pan': 'AJAYK1234L',
                'interested_project': 'Green Valley',
                'interested_plot': 'A-124',
                'booking_status': 'interested',
            },
            {
                'name': 'Pooja Mehra',
                'email': 'pooja.m@gmail.com',
                'password': 'Customer@123',
                'role': 'customer',
                'first_name': 'Pooja',
                'middle_name': '',
                'last_name': 'Mehra',
                'age': 29,
                'address': '222 Willow Ave',
                'phone': '9876543223',
                'adhar': '123456789023',
                'pan': 'POOJA5678M',
                'interested_project': 'Blue Heights',
                'interested_plot': 'B-457',
                'booking_status': 'interested',
            }
        ]
        # Assign reference_agent alternately between the two agents
        agent_u_ids = u_id_map['ag']
        for idx, cust_info in enumerate(customer_users):
            u_id = f"cs-{idx+1:010d}"
            reference_agent = agent_u_ids[idx % len(agent_u_ids)] if agent_u_ids else None
            user = User(
                first_name=cust_info['first_name'],
                last_name=cust_info['last_name'],
                email=cust_info['email'],
                password=generate_password_hash(cust_info['password']),
                dob=cust_info.get('dob', datetime(1990, 1, 1)),
                gender=cust_info.get('gender', 'Male'),
                adhar=cust_info['adhar'],
                pan=cust_info['pan'],
                aadhaar_file=cust_info.get('aadhaar_file', None),
                pan_file=cust_info.get('pan_file', None),
                designation=cust_info.get('designation', None),
                role=cust_info['role'],
                reference_agent=reference_agent,
                agent_team=cust_info.get('agent_team', None),
                mobile=cust_info.get('phone', None),
                u_id=u_id
            )
            db.session.add(user)
            db.session.commit()
            customer = Customer(
                user_id=user.u_id,
                first_name=cust_info['first_name'],
                middle_name=cust_info.get('middle_name', ''),
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
            ),
            Project(
                name='Sunrise Residency',
                description='Completed residential plots',
                location='Pune',
                start_date=datetime(2020, 1, 1),
                end_date=datetime(2022, 12, 31),
                status='completed',
                total_area=60000.0,
                developer='Sunrise Group'
            ),
            Project(
                name='Lakeview Enclave',
                description='Planning stage for lakeside homes',
                location='Hyderabad',
                start_date=datetime(2024, 1, 1),
                end_date=datetime(2026, 12, 31),
                status='planning',
                total_area=80000.0,
                developer='Lakeview Developers'
            )
        ]
        db.session.add_all(projects)
        db.session.commit()

        # Create Plots (multiple per project)
        plots = [
            # Green Valley
            Plot(
                project_id=projects[0].id,
                plot_number='A-123',
                size=2500.0,
                price=5000000.0,
                status='available'
            ),
            Plot(
                project_id=projects[0].id,
                plot_number='A-124',
                size=2600.0,
                price=5100000.0,
                status='sold'
            ),
            # Blue Heights
            Plot(
                project_id=projects[1].id,
                plot_number='B-456',
                size=3000.0,
                price=7500000.0,
                status='reserved'
            ),
            Plot(
                project_id=projects[1].id,
                plot_number='B-457',
                size=3200.0,
                price=7700000.0,
                status='available'
            ),
            # Sunrise Residency
            Plot(
                project_id=projects[2].id,
                plot_number='S-101',
                size=2000.0,
                price=4000000.0,
                status='sold'
            ),
            Plot(
                project_id=projects[2].id,
                plot_number='S-102',
                size=2100.0,
                price=4100000.0,
                status='available'
            ),
            # Lakeview Enclave
            Plot(
                project_id=projects[3].id,
                plot_number='L-201',
                size=3500.0,
                price=9000000.0,
                status='available'
            ),
            Plot(
                project_id=projects[3].id,
                plot_number='L-202',
                size=3600.0,
                price=9200000.0,
                status='available'
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
            Visit(
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