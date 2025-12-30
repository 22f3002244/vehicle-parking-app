# SpotKart - Vehicle Parking Spot Booking Application

A comprehensive web-based parking management system that enables users to find, book, and pay for parking spots while providing administrators with powerful management and analytics tools.

## ✨ Features

### User Dashboard

- **Real-time Availability**: View available parking spots across multiple cities
- **Instant Booking**: Reserve parking spots with immediate confirmation
- **Automatic Billing**: Duration-based charging with transparent pricing
- **Multi-Vehicle Support**: Register and manage multiple vehicles
- **History Tracking**: Access complete booking and payment history
- **Profile Management**: Secure account management with password protection

### Admin Dashboard

- **Spot Management**: Add, edit, and delete parking spots across different cities
- **User Management**: View and manage user accounts and registered vehicles
- **Visual Analytics**: Interactive charts and graphs powered by Plotly.js showing:
  - Booking distribution by city
  - User activity patterns
  - Vehicle registration statistics
  - Slot utilization metrics
  - Revenue trends and forecasts
- **Advanced Search**: Filter users by name, city, or vehicle details

## 🛠 Technologies Used

### Backend
- **Flask**: Python web framework
- **SQLAlchemy**: ORM for database operations
- **Werkzeug**: Security utilities for password hashing
- **Flask Blueprints**: Modular application structure

### Frontend
- **HTML5/CSS3**: Semantic markup and responsive styling
- **Bootstrap**: UI framework for responsive design
- **JavaScript**: Dynamic client-side interactions
- **Font Awesome**: Icon library
- **Plotly.js**: Interactive data visualizations

### Database
- **SQLite**: Lightweight relational database

## 📦 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Setup Instructions

1. Clone the repository:
```bash
git clone https://github.com/22f3002244/vehicle-parking-app.git
cd vehicle-parking-app
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

3. Install required dependencies:
```bash
pip install -r requirements.txt
```

4. Initialize the database:
```bash
python app.py
```

The application will automatically create the SQLite database in the `instance/` folder.

5. Access the application:
```
http://localhost:5000
```

## 🚀 Usage

### For Users

1. **Register**: Create an account with your email and password
2. **Add Vehicle**: Register your vehicle with license plate and details
3. **Find Parking**: Browse available spots by city and location
4. **Book Spot**: Select and reserve a parking spot
5. **Park**: Use the booking confirmation to access the parking spot
6. **Checkout**: Complete your parking session and view charges

### For Administrators

1. **Login**: Use admin credentials to access the admin dashboard
2. **Manage Spots**: Add new parking locations or modify existing ones
3. **Monitor Users**: View all registered users and their activities
4. **View Analytics**: Access detailed reports and visualizations
5. **Manage Bookings**: Oversee active and historical bookings

## 📁 Project Structure

```
vehicle-parking-app/
├── app.py                      # Main application entry point
├── requirements.txt            # Python dependencies
├── Project-Report.docx         # Detailed project documentation
├── controllers/                # Blueprint controllers
│   ├── bookings.py            # Booking management routes
│   ├── car.py                 # Vehicle registration routes
│   ├── control.py             # Admin control routes
│   ├── main.py                # General routes (home, auth)
│   ├── spot.py                # Parking spot routes
│   └── User.py                # User management routes
├── instance/
│   └── parking.db             # SQLite database (auto-generated)
├── models/
│   └── database.py            # Database models and schema
└── templates/                  # HTML templates
    ├── admin/                 # Admin dashboard templates
    ├── bookings/              # Booking-related templates
    ├── car/                   # Vehicle management templates
    ├── general/               # Login, register, home templates
    └── spots/                 # Parking spot templates
```

## 🔐 Authentication & Security

- **Session Management**: Secure session-based authentication using Flask sessions
- **Password Security**: Passwords are hashed using Werkzeug's security utilities
- **Role-Based Access**: Separate user and admin roles with restricted access
- **CSRF Protection**: Form submissions are protected against cross-site request forgery
- **Input Validation**: Server-side validation prevents malicious input

## 🔄 Core Workflows

### Booking Workflow

1. User browses available parking spots filtered by city
2. System validates that user has a registered vehicle
3. User selects a spot and confirms booking
4. Slot count is decremented in the database
5. Booking record is created with start time
6. User receives booking confirmation

### Checkout Workflow

1. User initiates checkout for active booking
2. System calculates parking duration (end time - start time)
3. Charges are computed based on hourly rate
4. Payment is recorded in the database
5. Parking slot is released and made available
6. Booking status is updated to inactive
7. Booking is added to user's history

### Admin Management Workflow

1. Admin logs in to dashboard
2. Can create new parking locations with city, address, and capacity
3. Can edit existing spot details (price, availability)
4. Can view all users and search by various criteria
5. Analytics are automatically generated from booking data

## 📊 Admin Analytics

The admin dashboard features interactive visualizations built with Plotly.js:

- **Booking Distribution**: Pie/bar charts showing bookings per city
- **User Activity**: Timeline of user registrations and activity
- **Vehicle Statistics**: Breakdown of registered vehicle types
- **Slot Utilization**: Occupancy rates across different locations
- **Revenue Analysis**: Financial performance over time
- **Peak Hours**: Identify high-demand time periods

## 🗄 Database Schema

### Key Tables

- **Users**: User accounts (id, email, password_hash, role)
- **Vehicles**: Registered vehicles (id, user_id, license_plate, model)
- **ParkingSpots**: Available parking locations (id, city, address, capacity, price)
- **Bookings**: Parking reservations (id, user_id, spot_id, start_time, end_time, active)
- **Payments**: Transaction records (id, booking_id, amount, timestamp)

View the complete database schema in the `models/database.py` file.

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is available for educational purposes. Please check with the repository owner for specific licensing terms.

## Author

Vedant Konde - vedantkonde09@gmail.com

---

**Note**: This is a student project developed as part of an academic assignment. For production use, additional security measures and scalability considerations should be implemented.
