from flask import Blueprint, request, jsonify

healthcheck_bp = Blueprint('healthcheck', __name__)

@healthcheck_bp.route('/', methods=['GET'])
def healthcheck():
    return jsonify({'status': 'OK'}), 200





