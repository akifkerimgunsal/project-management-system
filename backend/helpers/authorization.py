from flask import jsonify
from functools import wraps
from helpers.permissions import check_permission
from helpers.auth_helpers import get_current_user
from helpers.response_helpers import error_response
from entities import db

def authorize(required_roles):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            user = get_current_user()
            if not user:
                return error_response("Unauthorized", 401)

            entity_id = kwargs.get('entity_id')
            entity_type = kwargs.get('entity_type')
            if not entity_type or not entity_id:
                return error_response("Entity type or ID is missing", 400)

            entity = db.session.query(entity_type).get(entity_id)
            if not entity:
                return error_response(f"Entity not found: {entity_type} with ID {entity_id}", 404)

            try:
                check_permission(user, entity, required_roles)
            except PermissionError as e:
                return error_response(str(e), 403)

            return func(*args, **kwargs)
        return wrapper
    return decorator
