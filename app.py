from flask import Flask, request, jsonify
from pymongo import MongoClient
from flask_cors import CORS
import bcrypt 

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

client = MongoClient('mongodb://localhost:27017/')
db = client['horizon']
admins_collection = db['admins']
registrations = db['registrations']

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
    return jsonify({'message': 'Registration successful'}), 201

if __name__ == '__main__':
    app.run(debug=True)

