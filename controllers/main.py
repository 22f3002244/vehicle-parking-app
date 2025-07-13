from flask import redirect, url_for, flash, session
from models.database import User
from functools import wraps

def admin_required(func):
    @wraps(func)
    def inner (*args, **kwargs):
        if 'user_id' not in session:
                flash('You need to login first.')
                return redirect(url_for('User.login'))
        user = User.query.get(session['user_id'])
        if not user.is_admin:
            flash('You are not authorized to view this page.')
            return redirect(url_for('User.index'))
        return func(*args, **kwargs)
    return inner

def auth_required(func):
    @wraps(func)
    def inner (*args, **kwargs):
        if 'user_id' not in session:
            flash('You need to login first.')
            return redirect(url_for('User.login'))
        return func(*args, **kwargs)
    return inner 