from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from sqlalchemy import func
from models.database import User, Bookings, db, Spots, Car
from .main import admin_required, auth_required

user = Blueprint('User', __name__)

@user.route('/user')
@admin_required
def users():
        user=User.query.all()
        cars=Car.query.all()
        query = request.args.get('query')

        if query:
            cars = Car.query.join(User).filter(
                (User.id.ilike(f"%{query}%")) |
                (User.username.ilike(f"%{query}%")) | 
                (User.city.ilike(f"%{query}%")) | 
                (Car.plate_number.ilike(f"%{query}%"))
                ).all()
            if not cars:
                flash("Not Found")
        else:
            cars = Car.query.all()
        return render_template('admin/users.html', user=User.query.get(session['user_id']), users=user, car=cars, query=query)

@user.route('/admin')
@admin_required
def admin():
    user = User.query.get(session['user_id'])
    if not user.is_admin:
        flash('You are not authorized to view this page.')
        return redirect(url_for('User.index'))
        
    query = request.args.get('query')

    if query:
        spot = Spots.query.filter(
            (Spots.id.ilike(f"%{query}%")) |
            (Spots.name.ilike(f"%{query}%")) | 
            (Spots.city.ilike(f"%{query}%")) 
            ).all()
        if not spot:
            flash("Not Found")
    else:
        spot=Spots.query.all()
    return render_template('admin/admin.html', user=user, spot=spot)

@user.route('/analytics')
@admin_required
def analytics():
    user = User.query.get(session['user_id'])
    bookings_per_city = (
    db.session.query(Spots.city, func.count(Bookings.id))
    .join(Bookings, Bookings.spot_id == Spots.id)
    .group_by(Spots.city)
    .all()
    )

    bookings_per_user = (
    db.session.query(User.username, func.count(Bookings.id))
    .join(Bookings, Bookings.user_id == User.id)
    .group_by(User.username)
    .all()
    )

    vehicles_per_user = (
        db.session.query(User.username, func.count(Car.id))
        .join(Car, Car.user_id == User.id)
        .group_by(User.username)
        .all()
        )

    spots_per_city = (
        db.session.query(Spots.city, func.sum(Spots.no_of_slots))
        .group_by(Spots.city)
        .all()
    )

    data = {
        'cities_1': [x[0] for x in bookings_per_city],
        'counts_1': [x[1] for x in bookings_per_city],

        'users_2': [x[0] for x in bookings_per_user],
        'counts_2': [x[1] for x in bookings_per_user],

        'users_3': [x[0] for x in vehicles_per_user],
        'counts_3': [x[1] for x in vehicles_per_user],

        'cities_4': [x[0] for x in spots_per_city],
        'counts_4': [x[1] for x in spots_per_city],
    }

    return render_template('admin/analytics.html', **data, user=user)

@user.route('/login')
def login():
    return render_template('general/login.html')
    
@user.route('/register')
def Register():
    return render_template('general/register.html')
    
@user.route('/login', methods=['POST'])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')
    user = User.query.filter_by(username=username).first()
    if not user :
        flash ('User does not exist.')
        return redirect(url_for('User.login'))
    if not user.check_password(password):
        flash ('Incorrect Password.')
        return redirect(url_for('User.login'))
        
    session['user_id']=user.id
    if user.is_admin:
        return redirect(url_for('User.admin'))
    else:
        return redirect(url_for('User.index'))

@user.route('/register', methods=['POST'])
def register_post():
    name = request.form.get('name')
    username = request.form.get('username')
    password = request.form.get('password')
    city = request.form.get('city')
    if User.query.filter_by(username=username).first():
        flash('User with this username already exists. Please choose some other username.8u')
        return redirect(url_for('User.register'))
    user = User(username=username, password=password, name=name, city=city)
    db.session.add(user)
    db.session.commit()
    flash('User successfully registered.')
    return redirect(url_for('User.login'))

@user.route('/profile')
@auth_required
def profile():
    return render_template('general/profile.html', user=User.query.get(session['user_id']))
    
@user.route('/profile', methods=['POST'])
@auth_required
def profile_post():
    user = User.query.get(session['user_id'])
    username = request.form.get('username')
    name = request.form.get('name')
    city = request.form.get('city')
    password =  request.form.get('password')
    cpassword = request.form.get('cpassword')
    if username == ''  or password == '' or cpassword == '':
        flash('Username or password cannot be empty.')
        return redirect(url_for('User.profile'))
    if not user.check_password(cpassword):
        flash('Incorrect password.')
        return redirect(url_for('User.profile'))
    if User.query.filter_by(username=username).first() and username != user.username:
        flash('User with this username already exists. Please choose some other username.')
        return redirect(url_for('User.profile'))
    user.username = username
    user.name = name
    user.city = city
    user.password = password
    db.session.commit()
    flash('Profile updated successfully.')
    return redirect(url_for('User.profile'))

@user.route('/')
@auth_required
def index():
    user = User.query.get(session.get('user_id'))
    query = request.args.get('query')

    if user and user.is_admin:
        if query:
            spot = Spots.query.filter(
            (Spots.id.ilike(f"%{query}%")) |
            (Spots.name.ilike(f"%{query}%")) | 
            (Spots.city.ilike(f"%{query}%")) 
            ).all()
            
            if not spot:
                flash("Not Found")
        else:
            spot=Spots.query.all()
        return render_template('admin/admin.html', user=user, spot=spot)
    
    elif user:
        if not query:
            spot=Spots.query.all()
            bookings=Bookings.query.filter(Bookings.is_active == 1).order_by(Bookings.id.desc()).all()
            return render_template('general/index.html', user=user, spot=spot, bookings=bookings )
        else:
            spots = Spots.query.filter( (Spots.name.ilike(f"%{query}%")) | (Spots.city.ilike(f"%{query}%")) ).all()
            bookings=Bookings.query.filter(Bookings.is_active == 1).order_by(Bookings.id.desc()).all()
        return render_template('general/index.html', user=user, spot=spots, bookings=bookings)   
    
    else:
        return redirect('/login')
    
@user.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('User.login'))