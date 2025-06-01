from flask import render_template, request, redirect, url_for, flash, session, Blueprint
from models.database import db, User, Car
from .main import auth_required

car = Blueprint('car', __name__)

@car.route('/my_vehicle')
@auth_required
def my_vehicle():
        user = User.query.get(session['user_id'])
        return render_template('car/car.html', user=user, car=Car.query.filter_by(user_id=user.id).all()) 
    

@car.route('/vehicle/add')
@auth_required
def add_car():
        user = User.query.get(session['user_id'])
        return render_template('car/add.html', user=user)
    
@car.route('/vehicle/add', methods=['POST'])
@auth_required
def add_car_post():
        name = request.form.get('name')
        model = request.form.get('model')
        color = request.form.get('color')
        vehicle_number = request.form.get('vehicle_number')
        user = User.query.get(session['user_id'])

        if name == '' or model == '' or color == '' or vehicle_number == '':
            flash('Please fill all the details.')
            return redirect(url_for('add_car'))
        if len(name) > 64:
            flash('Vehicle name cannot be greater than 64 characters')
            return redirect(url_for('add_car'))
        
        existing_vehicle = Car.query.filter_by(plate_number=vehicle_number).first()
        if existing_vehicle:
            flash("Vehicle number already exists.")
            return redirect(url_for("car.add_car"))
        car = Car(name=name, model=model, color=color, plate_number=vehicle_number, user_id=user.id)
        db.session.add(car)
        db.session.commit()
        flash('Vehicle added successfully.')
        return redirect(url_for('car.my_vehicle', user=User.query.get(session['user_id'])))
    
@car.route('/vehicle/<int:id>/edit')
@auth_required
def edit_car(id):
        return render_template('car/edit.html', user=User.query.get(session['user_id']), car=Car.query.get(id))
    
@car.route('/vehicle/<int:id>/edit', methods=['POST'])
@auth_required
def edit_car_post(id):
        name = request.form.get('name')
        model = request.form.get('model')
        color = request.form.get('color')
        vehicle_number = request.form.get('vehicle_number')
        user = User.query.get(session['user_id'])
        
        if name == '' or model == '' or color == '' or vehicle_number == '':
            flash('Please fill all the details.')
            return redirect(url_for('car.edit_car'))
        if len(name) > 64:
            flash('Vehicle name cannot be greater than 64 characters')
            return redirect(url_for('car.edit_car'))
        car = Car.query.get(id)
        if not car:
            flash('Vehicle not found.')
            return redirect(url_for('car.add_car'))

        car.name = name
        car.model = model
        car.color = color
        car.plate_number = vehicle_number
        db.session.commit()
        flash('Details Updated successfully.')
        return redirect(url_for('car.my_vehicle'))

@car.route('/vehicle/<int:id>/delete')
@auth_required
def delete_car(id):
        return render_template('car/delete.html', user=User.query.get(session['user_id']), car=Car.query.get(id))
    
@car.route('/vehicle/<int:id>/delete', methods=['POST'])
@auth_required
def delete_car_post(id):
        user = User.query.get(session['user_id'])
        car = Car.query.get(id)
        if not car:
            flash('Vehiicle does not exist.')
            return redirect(render_template('car/car.html'))
        db.session.delete(car)
        db.session.commit()
        flash('Vehicle deleted successfully.')
        return redirect(url_for('car.my_vehicle'))
