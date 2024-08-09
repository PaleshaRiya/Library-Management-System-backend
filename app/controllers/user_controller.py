from flask import Blueprint, request, jsonify
from app.services.user_service import UserService
from app.decorators import admin_required

user_bp = Blueprint('user', __name__)
user_service = UserService()

@user_bp.route('/', methods=['GET'])
def get_all_users():
    filters = {
        'username': request.args.get('username'),
        'role': request.args.get('role'),
        'email': request.args.get('email'),
        'id': request.args.get('id')
    }
    # Remove keys with None values
    filters = {k: v for k, v in filters.items() if v is not None}
    
    users = user_service.get_all_users(filters)
    return jsonify([user.to_dict() for user in users])

@user_bp.route('/', methods=['POST'])
@admin_required
def create_user():
    try:
        user_data = request.json
        user_id = user_service.create_user(user_data)
        return jsonify({'id': user_id}), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@user_bp.route('/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user_data = request.json
    try:
        user_service.update_user(user_id, user_data)
        return jsonify({'message': 'User updated'})
    except ValueError as e:
        return jsonify({'error': str(e)}), 404

@user_bp.route('/<int:user_id>', methods=['DELETE'])
@admin_required
def delete_user(user_id):
    user_service.delete_user(user_id)
    return jsonify({'message': 'User deleted'})

@user_bp.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response