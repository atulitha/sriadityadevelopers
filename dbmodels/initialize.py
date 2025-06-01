from datetime import datetime, timedelta

from flask import Flask

from dbmodels.create import (
    db, Customer, Agent, Project, Plot,
    booking, visit, feedback
)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../../users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


def init_db():
    with app.app_context():
        db.create_all()

        # Create Agents
        agents = [
            Agent(
                first_name='John', middle_name='Robert', last_name='Doe',
                position='Senior Agent', office='Mumbai',
                age=35, Address='123 Main St',
                start_date=datetime(2022, 1, 1),
                percentage=10, sales=500000.0,
                status='Full-time', email='john.doe@example.com',
                phone='9876543210', adhar='123456789012',
                pan='ABCDE1234F', password='hashed_password',
                role='agent'
            ),
            Agent(
                first_name='Jane', middle_name='Marie', last_name='Smith',
                position='Agent', office='Delhi',
                age=28, Address='456 Oak Ave',
                start_date=datetime(2022, 6, 1),
                percentage=8, sales=300000.0,
                status='Part-time', email='jane.smith@example.com',
                phone='9876543211', adhar='123456789013',
                pan='FGHIJ5678K', password='hashed_password',
                role='agent'
            )
        ]
        db.session.add_all(agents)
        db.session.commit()

        # Create Customers
        customers = [
            Customer(
                first_name='Mike', middle_name='Thomas', last_name='Johnson',
                age=45, address='789 Pine Rd',
                email='mike.j@example.com', phone='9876543212',
                adhar='123456789014', pan='KLMNO9012P',
                interested_project='Green Valley',
                interested_plot='A-123',
                booking_status='interested',
                password='hashed_password'
            ),
            Customer(
                first_name='Sarah', middle_name='Elizabeth', last_name='Wilson',
                age=32, address='321 Cedar Ln',
                email='sarah.w@example.com', phone='9876543213',
                adhar='123456789015', pan='QRSTU3456V',
                interested_project='Blue Heights',
                interested_plot='B-456',
                booking_status='booked',
                password='hashed_password'
            )
        ]
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
    init_db()
    print("Database initialized successfully with mock data!")