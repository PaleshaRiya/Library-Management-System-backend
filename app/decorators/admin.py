from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        ans = verify_jwt_in_request()
        
        if not ans:
            return jsonify(message='Missing or invalid token'), 401
                
        current_role = ans[1]['role']

        if current_role != 'ADMIN':
            return jsonify(message='Admin role required to access this endpoint'), 403

        return fn(*args, **kwargs)

    return wrapper
