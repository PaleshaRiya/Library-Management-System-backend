from flask import Blueprint, request, jsonify
from app.services import FeedbackService
from app.decorators import admin_required

feedback_bp = Blueprint('feedback', __name__)
feedback_service = FeedbackService()

@feedback_bp.route('/', methods=['GET'])
def get_all_feedbacks():
    filters = {
        'id' : request.args.get('id'),
        'userId' : request.args.get('userId'),
        'bookId' : request.args.get('bookId')
    }
    # Remove keys with None values
    filters = {k: v for k, v in filters.items() if v is not None}
    
    feedbacks = feedback_service.get_all_feedbacks(filters)
    return jsonify([feedback.to_dict() for feedback in feedbacks])

@feedback_bp.route('/', methods=['POST'])
def create_feedback():
    try:
        feedback_data = request.json
        feedback_id = feedback_service.create_feedback(feedback_data)
        return jsonify({'message': "Feedback created"}), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@feedback_bp.route('/<int:feedback_id>', methods=['PUT'])
def update_feedback(feedback_id):
    feedback_data = request.json
    try:
        feedback_service.update_feedback(feedback_id, feedback_data)
        return jsonify({'message': 'feedback updated'})
    except ValueError as e:
        return jsonify({'error': str(e)}), 404

@feedback_bp.route('/<int:feedback_id>', methods=['DELETE'])
def delete_feedback(feedback_id):
    feedback_service.delete_feedback(feedback_id)
    return jsonify({'message': 'feedback deleted'})

@feedback_bp.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response