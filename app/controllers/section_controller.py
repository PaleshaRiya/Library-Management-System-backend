from flask import Blueprint, request, jsonify
from app.services.section_service import SectionService
from app.decorators import admin_required

section_bp = Blueprint('section', __name__)
section_service = SectionService()

@section_bp.route('/', methods=['GET'])
def get_all_sections():
    filters = {
        'name': request.args.get('name'),
        'id' : request.args.get('id')
    }
    # Remove keys with None values
    filters = {k: v for k, v in filters.items() if v is not None}
    
    sections = section_service.get_all_sections(filters)
    return jsonify([section.to_dict() for section in sections])

@section_bp.route('/', methods=['POST'])
@admin_required
def create_section():
    try:
        section_data = request.json
        section_id = section_service.create_section(section_data)
        return jsonify({'id': section_id}), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@section_bp.route('/<int:section_id>', methods=['PUT'])
@admin_required
def update_section(section_id):
    section_data = request.json
    try:
        section_service.update_section(section_id, section_data)
        return jsonify({'message': 'section updated'})
    except ValueError as e:
        return jsonify({'error': str(e)}), 404

@section_bp.route('/<int:section_id>', methods=['DELETE'])
@admin_required
def delete_section(section_id):
    section_service.delete_section(section_id)
    return jsonify({'message': 'section deleted'})


@section_bp.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response