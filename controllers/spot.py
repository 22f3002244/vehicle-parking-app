from flask import render_template, request, redirect, url_for, flash, session, Blueprint
from models.database import db, User, Spots
from .main import admin_required, auth_required

spot = Blueprint('spot', __name__)

@spot.route('/slot/add')
@admin_required
def add_slot():
    return render_template('spots/add.html', user=User.query.get(session['user_id']) )
    
@spot.route('/slot/add', methods=['POST'])
@admin_required
def add_slot_post():
        name = request.form.get('name')
        city = request.form.get('city')
        available = request.form.get('available')
        charges = request.form.get('charges')

        if name == '' or city == '' or available == '' or charges == '':
            flash('Please fill all the details.')
            return redirect(url_for('add_slot'))
        if len(name) > 64:
            flash('Spot name cannot be greater than 64 characters')
            return redirect(url_for('add_slot'))
        spot = Spots(name=name, city=city, no_of_slots=available, charges=charges)
        db.session.add(spot)
        db.session.commit()
        flash('Spot added successfully.')
        return redirect(url_for('User.admin', user=User.query.get(session['user_id'])))
    
@spot.route('/spot/<int:id>/edit')
@admin_required
def edit_spot(id):
        return render_template('spots/edit.html', user=User.query.get(session['user_id']), spot=Spots.query.get(id))
    
@spot.route('/spot/<int:id>/edit', methods=['POST'])
@admin_required
def edit_spot_post(id):
        name = request.form.get('name')
        city = request.form.get('city')
        available = request.form.get('available')
        charges = request.form.get('charges')
        
        if name == '' or city == '' or available == '' or charges == '':
            flash('Please fill all the details.')
            return redirect(url_for('add_slot'))
        if len(name) > 64:
            flash('Spot name cannot be greater than 64 characters')
            return redirect(url_for('add_slot'))
        spot = Spots.query.get(id)
        if not spot:
            flash('Spot not found.')
            return redirect(url_for('User.admin'))

        spot.name = name
        spot.city = city
        spot.no_of_slots = available
        spot.charges = charges
        db.session.commit()
        flash('Spot Updated successfully.')
        return redirect(url_for('User.admin', user=User.query.get(session['user_id'])))

@spot.route('/spot/<int:id>/delete')
@admin_required
def delete_spot(id):
        return render_template('spots/delete.html', user=User.query.get(session['user_id']), spot=Spots.query.get(id))
    
@spot.route('/spot/<int:id>/delete', methods=['POST'])
@admin_required
def delete_spot_post(id):
        spot = Spots.query.get(id)
        if not spot:
            flash('Spot does not exist.')
            return redirect(url_for('User.admin'))
        db.session.delete(spot)
        db.session.commit()
        flash('Spot deleted successfully.')
        return redirect(url_for('User.admin', user=User.query.get(session['user_id'])))
    