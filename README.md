# vehicle-parking-app
SpotKart - A car parking spot booking application.

## Features

### User Dashboard

* Real-time slot availability and instant booking
* Automatic billing based on parking duration
* Support for registering multiple vehicles
* Booking and payment history tracking
* Secure profile management

### Admin Dashboard

* Add, edit, and delete parking spots across cities
* View and manage users and their vehicles
* Visual analytics for bookings, usage, and revenue using Plotly.js
* Search and filter users by name, city, or vehicle details

## Technologies Used

* Backend: Flask, SQLAlchemy, Werkzeug, Flask Blueprints
* Frontend: HTML, CSS, Bootstrap, JavaScript, Font-Awesome, Plotly.js
* Database: SQLite

## Authentication and Security

* Session-based login using Flask sessions
* Password hashing using Werkzeug
* Role-based access control (admin/user)
* CSRF protection and input validation

## Folder Structure
'''
project/
├── app.py
├── requirements.txt
├── controllers/
│   ├── bookings.py
│   ├── car.py
│   ├── control.py
│   ├── main.py
│   ├── spot.py
│   └── User.py
├── instance/
│   └── parking.db
├── models/
│   └── database.py
└── templates/
    ├── admin/
    ├── bookings/
    ├── car/
    ├── general/
    └── spots/
'''


## Core Workflows

### Booking Flow

1. User selects an available spot
2. System validates vehicle registration
3. Slot count is decremented and booking is recorded
4. User receives booking confirmation

### Checkout Flow

1. System calculates duration of parking
2. Charges are applied based on hourly rate
3. Payment is recorded and slot is released
4. Booking is marked inactive and added to history

## Admin Analytics (via Plotly.js)

* Booking distribution by city
* User activity patterns
* Vehicle registration statistics
* Slot utilization per location
* Revenue trends

## Project Video Demo

Link: https://drive.google.com/file/d/1x_q0CbEFqPTyPl8PsEaVF7_q0ZcqepG8/view
