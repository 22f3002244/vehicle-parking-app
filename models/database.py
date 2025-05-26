from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user' 
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, nullable=False)
    password_hash = db.Column(db.String(512), nullable=False)
    name = db.Column(db.String(32), nullable=False)
    city = db.Column(db.String(32), nullable=False)
    is_admin = db.Column(db.Boolean, nullable = False, default = False)

    car = db.relationship('Car', backref='user', lazy=True)
    bookings = db.relationship('Bookings', backref='user', lazy=True)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute.')
    
    @password.setter
    def password(self, plaintext_password):
        self.password_hash = generate_password_hash(plaintext_password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Car(db.Model):
    __tablename__ = 'car'
    id = db.Column(db.Integer, primary_key=True)
    plate_number = db.Column(db.String(32), unique=True, nullable=False)
    model = db.Column(db.String(512), nullable=False)
    name = db.Column(db.String(32), nullable=False)
    color = db.Column(db.String(32), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    bookings = db.relationship('Bookings', backref='car', lazy=True)

class Spots(db.Model):
    __tablename__ = 'spot'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    city = db.Column(db.String(32), nullable=False)
    no_of_slots = db.Column(db.Integer, nullable=False)
    charges = db.Column(db.Integer, nullable=False)

    bookings = db.relationship('Bookings', backref='spot', lazy=True)

class Bookings(db.Model):
    __tablename__ = 'bookings'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    spot_id = db.Column(db.Integer, db.ForeignKey('spot.id'), nullable=False)
    car_id = db.Column(db.Integer, db.ForeignKey('car.id'), nullable=False)
    booking_date = db.Column(db.Date, nullable=False)
    booking_time = db.Column(db.Time, nullable=False)
    is_active = db.Column(db.Boolean, nullable = False, default = True)

    checkout = db.relationship('checkout', backref='booking', uselist=False, lazy=True)
    
class Checkout(db.Model):
    __tablename__='checkout'
    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('bookings.id'), nullable=False)
    exit_date = db.Column(db.Date, nullable=False)
    exit_time = db.Column(db.Time, nullable=False)
    payable_amount = db.Column(db.Integer, nullable=False)
    paid = db.Column(db.Boolean, nullable = False, default = True)