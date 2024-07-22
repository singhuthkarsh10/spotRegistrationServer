# Horizon '24 Registration and Admin Panel

This is a Flask application for managing registrations and admin logins for Horizon '24 event. The application integrates with MongoDB for data storage, Flask-Mail for sending emails, and generates QR codes for event tickets.

## Features

- Admin registration and login
- Event registration with QR code generation
- Email confirmation with QR code attachment
- CORS support

## Prerequisites

- Python 3.6+
- MongoDB Atlas account
- Gmail account for sending emails

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/your-username/horizon24-registration.git
    cd horizon24-registration
    ```

2. Create and activate a virtual environment:
    ```sh
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

4. Set up your MongoDB Atlas connection:
    Replace `username` and `password` in the script with your MongoDB Atlas credentials.

5. Configure Flask-Mail:
    Replace `MAIL_USERNAME` and `MAIL_PASSWORD` with your Gmail credentials in the script.

## Configuration

Update the following variables in the script:

- MongoDB credentials:
    ```python
    username = 'your_mongodb_username'
    password = 'your_mongodb_password'
    ```

- Flask-Mail configuration:
    ```python
    app.config['MAIL_USERNAME'] = 'your_email@gmail.com'
    app.config['MAIL_PASSWORD'] = 'your_email_password'
    ```

## Running the Application

1. Start the Flask application:
    ```sh
    python app.py
    ```

2. The application will run on `http://0.0.0.0:5001`.
