from flask import Blueprint, request, jsonify
from app.services import EbookService
from app.decorators import admin_required

ebook_bp = Blueprint('ebook', __name__)
ebook_service = EbookService()

@ebook_bp.route('/', methods=['GET'])
def get_all_ebooks():
    filters = {
        'name': request.args.get('name'),
        'id' : request.args.get('id'),
        'sectionId': request.args.get('sectionId')
    }
    # Remove keys with None values
    filters = {k: v for k, v in filters.items() if v is not None}
    
    ebooks = ebook_service.get_all_ebooks(filters)
    return jsonify([ebook.to_dict() for ebook in ebooks])

@ebook_bp.route('/', methods=['POST'])
@admin_required
def create_ebook():
    try:
        ebook_data = request.json
        ebook_id = ebook_service.create_ebook(ebook_data)
        return jsonify({'id': ebook_id}), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@ebook_bp.route('/<int:ebook_id>', methods=['PUT'])
@admin_required
def update_ebook(ebook_id):
    ebook_data = request.json
    try:
        ebook_service.update_ebook(ebook_id, ebook_data)
        return jsonify({'message': 'ebook updated'})
    except ValueError as e:
        return jsonify({'error': str(e)}), 404

@ebook_bp.route('/<int:ebook_id>', methods=['DELETE'])
@admin_required
def delete_ebook(ebook_id):
    ebook_service.delete_ebook(ebook_id)
    return jsonify({'message': 'ebook deleted'})

@ebook_bp.route('/<int:ebook_id>/section/<int:section_id>', methods=['POST'])
@admin_required
def add_ebook_to_section(ebook_id, section_id):
    try:
        ebook_service.add_ebook_to_section(ebook_id, section_id)
        return jsonify({'message': 'Ebook added to section'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@ebook_bp.route('/<int:ebook_id>/section/<int:section_id>', methods=['DELETE'])
@admin_required
def remove_ebook_from_section(ebook_id, section_id):
    try:
        ebook_service.remove_ebook_from_section(ebook_id, section_id)
        return jsonify({'message': 'Ebook removed from section'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@ebook_bp.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response