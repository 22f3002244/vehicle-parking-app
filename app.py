from flask import Flask
from models.database import db, User
from controllers.control import register_routes

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///parking.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'secretkey123'

db.init_app(app)
register_routes(app)


with app.app_context():
    db.create_all()

    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(
            username='admin',
            name='admin',
            city='Mumbai',
            contact='1234567890',
            email='22f3002244@ds.study.iitm.ac.in',
            is_admin=True
        )
        admin.password = 'admin'
        db.session.add(admin)
        db.session.commit()

    db.create_all()

    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(username='admin', password='admin', name='admin', city='Mumbai', contact='1234567890', email='22f3002244@ds.study.iitm.ac.in', is_admin=True)
        db.session.add(admin)
        db.session.commit()

if __name__ == "__main__":
    app.run(debug=True)