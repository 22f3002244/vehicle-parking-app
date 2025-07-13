from flask import render_template, request, redirect, url_for, flash, session, Blueprint
from models.database import db, User, Car, Spots, Bookings, Checkout
from datetime import datetime
from .main import auth_required
from math import ceil

book = Blueprint('bookings', __name__)

@book.route('/book_slot/<int:id>', methods=['GET', 'POST'])
@auth_required
def book_slot(id):
    user = User.query.get(session['user_id'])
    car = Car.query.filter_by(user_id=user.id).all()
    spot = Spots.query.get(id)

    if not car:
        flash("Please add your vehicle before booking a slot.")
        return redirect(url_for('car.add_car'))

    if request.method == 'POST':
        vehicle_id = request.form.get('vehicle_id')
        active_booking = Bookings.query.filter_by(car_id=vehicle_id, is_active=True).first()
        if active_booking:
            flash("This vehicle is already parked with an active booking. Please checkout before booking again.")
            return redirect(url_for('User.index'))

        current = datetime.now()
        date = current.date()
        time = current.time()

        spot.no_of_slots -= 1

        booking = Bookings(
            user_id=user.id,
            spot_id=spot.id,
            car_id=vehicle_id,
            booking_date=date,
            booking_time=time,
            is_active=True
        )
        db.session.add(booking)
        db.session.commit()

        return redirect(url_for('User.index'))

    return render_template('bookings/book.html', user=user, id=id, car=car, spot=spot)

@book.route('/check_out/<int:id>', methods=['POST'])
@auth_required
def check_out(id):
        user = User.query.get(session['user_id'])
        book= Bookings.query.get(id)

        booking_time = datetime.combine(book.booking_date, book.booking_time)
        current= datetime.now()

        duration = (current - booking_time).total_seconds()

        hours = int(duration // 3600)
        minutes = int((duration % 3600) // 60)
        exact_time_for_pay= ceil(duration / 3600)

        charges = book.spot.charges
        amount = (duration/3600) * (charges)

        date = current.date()
        time = current.time()

        check = Checkout( booking_id=book.id, exit_date=date, exit_time=time, payable_amount=amount, paid=True)
        db.session.add(check)
        db.session.commit()
        
        return render_template('bookings/checkout.html', user=user, c=book, date=date, time=time, duration=exact_time_for_pay, hour=hours, min=minutes, amount=amount)
    
@book.route('/pay/<int:id>', methods=['POST'])
@auth_required
def pay(id):
        booking = Bookings.query.get(id)
        booking.is_active = False
        spot = Spots.query.get(booking.spot_id)
        spot.no_of_slots += 1
        db.session.commit()
        flash("Payment successful.")
        return redirect(url_for('User.index'))
    
@book.route('/booking_history')
@auth_required
def bookings():
        user = User.query.get(session['user_id'])
        book = Bookings.query.filter_by(user_id=user.id, is_active=False).order_by(Bookings.id.desc()).all()
        return render_template('bookings/bookings.html', user=user, book=book)
