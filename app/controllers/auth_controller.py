# app/controllers/auth.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, JWTManager, decode_token
from app.services.user_service import UserService

auth_bp = Blueprint('auth', __name__)
user_service = UserService()

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    user = user_service.authenticate_user(username, password)

    if not user:
        print("Authentication failed")  # Debugging line
        return jsonify({'msg': 'Invalid username or password'}), 401

    access_token = create_access_token(identity=user.username, additional_claims={'role': user.role}, expires_delta=False)
    
    return jsonify(access_token=access_token, user_id=user.id)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    user_id = user_service.create_user(data)
    user = user_service.authenticate_user(data['username'], data['password'])
    
    if not user:
        print("Authentication failed")  # Debugging line
        return jsonify({'msg': 'Invalid username or password'}), 401

    access_token = create_access_token(identity=user.username, additional_claims={'role': user.role}, expires_delta=False)
    
    return jsonify(access_token=access_token, user_id=user_id)


@auth_bp.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response