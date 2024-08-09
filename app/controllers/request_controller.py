from flask import Blueprint, request, jsonify
from app.services.request_service import RequestService
from app.tasks.celeryworker import export_ebooks_csv
from app.decorators import admin_required

request_bp = Blueprint('request', __name__)
request_service = RequestService()


@request_bp.route('/', methods=['GET'])
def get_all_requests():
    filters = {
        'id' : request.args.get('id'),
        'userId' : request.args.get('userId'),
        'bookId' : request.args.get('bookId'),
        'isApproved' : request.args.get('isApproved'),
        'isRejected' : request.args.get('isRejected'),
        'isReturned' : request.args.get('isReturned'),
        'isRevoked' : request.args.get('isRevoked'),
        'isBought' : request.args.get('isBought'),
        'isDeleted' : request.args.get('isDeleted'),
        'issueDateFrom' : request.args.get('issueDateFrom'),
        'issueDateTo' : request.args.get('issueDateTo'),
        'returnDateFrom' : request.args.get('returnDateFrom'),
        'returnDateTo' : request.args.get('returnDateTo')
    }
    # Remove keys with None values
    filters = {k: v for k, v in filters.items() if v is not None}
    
    requests = request_service.get_all_requests(filters)
    return jsonify([request.to_dict() for request in requests])

@request_bp.route('/', methods=['POST'])
def create_request():
    try:
        request_data = request.json
        request_id = request_service.create_request(request_data)
        return jsonify({'id': request_id}), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@request_bp.route('/<int:request_id>', methods=['PUT'])
@admin_required
def update_request(request_id):
    request_data = request.json
    try:
        request_service.update_request(request_id, request_data)
        return jsonify({'message': 'request updated'})
    except ValueError as e:
        return jsonify({'error': str(e)}), 404

@request_bp.route('/return/<int:request_id>', methods=['PUT'])
def return_book(request_id):
    request_data = request.json
    try:
        request_service.return_book(request_id, request_data)
        return jsonify({'message': 'request updated'})
    except ValueError as e:
        return jsonify({'error': str(e)}), 404

@request_bp.route('/<int:request_id>', methods=['DELETE'])
def delete_request(request_id):
    request_service.delete_request(request_id)
    return jsonify({'message': 'request deleted'})

@request_bp.route('/export', methods=['GET'])
def export_requests():
    export_ebooks_csv.delay()
    return jsonify({'message': 'Export job started'}), 202

@request_bp.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response