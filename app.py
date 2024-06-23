from flask import Flask, request, jsonify, send_file
from pymongo import MongoClient
from flask_cors import CORS
import bcrypt 
from flask_mail import Mail, Message
import qrcode
from io import BytesIO

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

client = MongoClient('mongodb://localhost:27017/')
db = client['horizon']
admins_collection = db['admins']
registrations = db['registrations']

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'sptrgstrtn@gmail.com'  
app.config['MAIL_PASSWORD'] = 'apxdebntrqetleoo'         

mail = Mail(app)

@app.route('/', methods=['GET'])
def index():
    return 'Hello'

@app.route('/api/nafisa', methods=['POST'])
def createAdmin():
    data = request.json
    name = data.get('name')
    userID = data.get('userID')
    password = data.get('password')

    filter = {'userID' : userID}
    existingUser = admins_collection.find_one(filter)
    if existingUser:
        return jsonify({'message' : 'user already exists'}), 409

    hashedPass = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    newUser = {
        'name': name,
        'userID' : userID,
        'password' : hashedPass
    }

    admins_collection.insert_one(newUser)

    return jsonify({'message' : 'New user created successfully'}), 201

@app.route('/api/login', methods=['POST'])
def handle_login():
    data = request.json
    userID = data.get('userID')
    password = data.get('password')

    if not userID or not password:
        return jsonify({'message': 'Missing email or password'}), 400

    filter = {'userID' : userID}
    user=admins_collection.find_one(filter)
    if not user:
        return jsonify({'message' : 'Invalid user'}), 401

    if bcrypt.checkpw(password.encode('utf-8'), user['password']):
        return jsonify({'message' : 'Login successful'}), 200
    else:
        return jsonify({'message' : 'Invalid email or password'}), 401

@app.route('/api/registration', methods=['POST'])
def handle_registration():
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type',
        }
        return '', 200, headers

    data = request.json

    # Validate required fields
    required_fields = ['name', 'registerNo', 'email', 'department', 'section', 'mobileNumber', 
                       'dropdownValue', 'dropdownTxValue', 'transactionId']
    for field in required_fields:
        if field not in data or data[field].strip() == '':
            return jsonify({'message': f'Missing or empty {field} in request data'}), 400

    # Insert registration data into MongoDB
    registrations.insert_one(data)

    # Generate QR code
    qr_data = f"Name: {data['name']}\nRegister No: {data['registerNo']}\nEmail: {data['email']}\nDepartment: {data['department']}\nSection: {data['section']}\nMobile Number: {data['mobileNumber']}\nYear: {data['dropdownValue']}\nPayment Type: {data['dropdownTxValue']}\nEvent: {data['dropdownEventValue']} "

    qr_img = generate_qr(qr_data)
    
    # Send registration email with QR code
    send_registration_email(data['name'], data['email'], qr_img,data['dropdownEventValue'])

    return jsonify({'message': 'Registration successful'}), 201

def generate_qr(data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    return img

def send_registration_email(name, email, qr_img, event):
    img_bytes = BytesIO()
    qr_img.save(img_bytes, format='PNG')
    img_bytes = img_bytes.getvalue()
    msg = Message('Horizon \'24 Registration Confirmation', sender='sptrgstrtn@gmail.com', recipients=[email])
    msg.body = f'Hello {name},\n\nWelcome to Horizon 2024. Thank you for registering for the event {event}. We have attached a ticket with this email, you can show that ticket at the venue and proceed for the event.\n\nThanks and regards,\nACM SIST Student Chapter'

    msg.attach("ticket.png", "image/png", img_bytes)
    mail.send(msg)

if __name__ == '__main__':
    app.run(debug=True)
