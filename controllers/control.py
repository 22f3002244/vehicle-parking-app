from .User import user
from .car import car
from .spot import spot 
from .bookings import book

def register_routes(app):
    app.register_blueprint(user)
    app.register_blueprint(car)
    app.register_blueprint(spot)
    app.register_blueprint(book)