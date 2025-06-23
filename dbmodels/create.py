from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Customer(db.Model):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(20), db.ForeignKey('users.u_id'), nullable=False)  # Link to users.u_id
    first_name = db.Column(db.String(100), nullable=False)
    middle_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer)
    address = db.Column(db.String(200))
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), unique=True, nullable=False)
    adhar = db.Column(db.String(20), unique=True, nullable=False)
    pan = db.Column(db.String(20), unique=True, nullable=False)
    interested_project = db.Column(db.String(150))
    interested_plot = db.Column(db.String(50))
    booking_status = db.Column(db.String(50), default='interested')  # interested, booked, cancelled
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    role = db.Column(db.String(50), default='customer')
    user = db.relationship('User', backref='customer', lazy=True)


class Admin(db.Model):
    __tablename__ = 'admins'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(20), db.ForeignKey('users.u_id'), nullable=False)  # Link to users.u_id
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.relationship('User', backref='admin', lazy=True)


class Agent(db.Model):
    __tablename__ = 'agents'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(20), db.ForeignKey('users.u_id'), nullable=False)  # Link to users.u_id
    first_name = db.Column(db.String(100), nullable=False)
    middle_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(100), default='Agent')
    office = db.Column(db.String(100), default='Remote')
    age = db.Column(db.Integer)
    Address = db.Column(db.String(100))
    start_date = db.Column(db.Date, default=datetime.utcnow)
    percentage = db.Column(db.Integer)  # percentage of salary.
    sales = db.Column(db.Float, default=0.0)  # sales amount
    status = db.Column(db.String(50), default='Full-time')
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), unique=True, nullable=False)
    adhar = db.Column(db.String(20), unique=True, nullable=False)
    pan = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    role = db.Column(db.String(50), default='user')
    user = db.relationship('User', backref='agent', lazy=True)


class Project(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    location = db.Column(db.String(200))
    start_date = db.Column(db.Date, default=datetime.utcnow)
    end_date = db.Column(db.Date)
    status = db.Column(db.String(50), default='ongoing')  # 'ongoing', 'completed', 'planning'
    total_area = db.Column(db.Float)  # in sq ft or meters
    developer = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    plots = db.relationship('Plot', backref='project', lazy=True)


class Plot(db.Model):
    __tablename__ = 'plots'
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    plot_number = db.Column(db.String(50), nullable=False)
    size = db.Column(db.Float)  # size in square feet or meters
    price = db.Column(db.Float)  # price of the plot
    status = db.Column(db.String(50), default='available')  # 'available', 'sold', 'reserved'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)


class booking(db.Model):
    __tablename__ = 'bookings'
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    plot_id = db.Column(db.Integer, db.ForeignKey('plots.id'), nullable=False)
    booking_date = db.Column(db.Date, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    customer = db.relationship('Customer', backref='bookings', lazy=True)
    plot = db.relationship('Plot', backref='bookings', lazy=True)
    status = db.Column(db.String(50), default='pending')  # 'pending', 'confirmed', 'cancelled', registered
    amount = db.Column(db.Float, nullable=False)  # booking amount
    payment_status = db.Column(db.String(50), default='unpaid')  # 'unpaid', 'paid', 'refunded'
    payment_date = db.Column(db.DateTime)  # date of payment if paid
    agent_id = db.Column(db.Integer, db.ForeignKey('agents.id'), nullable=False)
    agent = db.relationship('Agent', backref='bookings', lazy=True)


class Visit(db.Model):
    __tablename__ = 'visits'
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    plot_id = db.Column(db.Integer, db.ForeignKey('plots.id'), nullable=False)
    agent_id = db.Column(db.Integer, db.ForeignKey('agents.id'), nullable=True)
    visit_date = db.Column(db.Date, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    customer = db.relationship('Customer', backref='visits', lazy=True)
    purpose = db.Column(db.String(200))  # purpose of the visit
    feedback = db.Column(db.Text)  # feedback from the visit
    status = db.Column(db.String(50), default='scheduled')  # 'scheduled', 'completed', 'cancelled'


class feedback(db.Model):
    __tablename__ = 'feedbacks'
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    feedback_date = db.Column(db.Date, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    customer = db.relationship('Customer', backref='feedbacks', lazy=True)
    comments = db.Column(db.Text)  # feedback comments
    rating = db.Column(db.Integer)  # rating out of 5
    status = db.Column(db.String(50), default='new')  # 'new', 'addressed', 'resolved'


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    dob = db.Column(db.Date, nullable=True)
    gender = db.Column(db.String(20), nullable=True)
    adhar = db.Column(db.String(20), unique=True, nullable=True)
    pan = db.Column(db.String(20), unique=True, nullable=True)
    aadhaar_file = db.Column(db.LargeBinary, nullable=True)  # Store file as binary  # Store file as binary
    pan_file = db.Column(db.LargeBinary, nullable=True)  # Store file as binary
    designation = db.Column(db.String(100), nullable=True)  # e.g., 'Director', 'Manager', 'Team Lead', 'Senior Agent', 'Agent'
    role = db.Column(db.String(50), default='user')  # 'customer', 'agent', 'admin'
    reference_agent = db.Column(db.String(100), nullable=True)  # Reference agent for agents
    agent_team = db.Column(db.String(100), nullable=True)  # Team for agents
    photo = db.Column(db.LargeBinary, nullable=True)  # Store photo as binary
    mobile = db.Column(db.String(20), unique=True, nullable=True)
    u_id = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(300), nullable=True)