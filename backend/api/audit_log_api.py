from flask import Blueprint, request
from entities import db
from entities.audit_log import AuditLog
from helpers.response_helpers import success_response, error_response
from helpers.auth_helpers import get_current_user

audit_log_bp = Blueprint('audit_log', __name__)

@audit_log_bp.route('/', methods=['GET'])
def get_logs():
    """
    İşlem kayıtlarını listele.
    """
    user = get_current_user()
    if not user:
        return error_response("Unauthorized", 401)

    # Filtreleme ve arama
    entity_type = request.args.get('entity_type')
    action = request.args.get('action')
    user_id = request.args.get('user_id')

    query = AuditLog.query

    if entity_type:
        query = query.filter(AuditLog.entity_type == entity_type)
    if action:
        query = query.filter(AuditLog.action == action)
    if user_id:
        query = query.filter(AuditLog.user_id == user_id)

    logs = query.order_by(AuditLog.timestamp.desc()).all()
    return success_response(data=[log.to_dict() for log in logs], message="Logs retrieved successfully.")

@audit_log_bp.route('/<int:log_id>', methods=['GET'])
def get_log(log_id):
    """
    Belirli bir işlem kaydını getir.
    """
    user = get_current_user()
    if not user:
        return error_response("Unauthorized", 401)

    log = AuditLog.query.get(log_id)
    if not log:
        return error_response("Log not found.", 404)

    return success_response(data=log.to_dict(), message="Log retrieved successfully.")

@audit_log_bp.route('/', methods=['POST'])
def create_log():
    """
    Yeni bir işlem kaydı oluştur.
    """
    user = get_current_user()
    if not user:
        return error_response("Unauthorized", 401)

    data = request.get_json()
    entity_id = data.get('entity_id')
    entity_type = data.get('entity_type')
    action = data.get('action')
    details = data.get('details', '')

    if not all([entity_id, entity_type, action]):
        return error_response("All fields are required: entity_id, entity_type, action.", 400)

    new_log = AuditLog(
        user_id=user.id,
        entity_id=entity_id,
        entity_type=entity_type,
        action=action,
        details=details
    )

    db.session.add(new_log)
    db.session.commit()

    return success_response(data=new_log.to_dict(), message="Log created successfully.", status=201)

@audit_log_bp.route('/<int:log_id>', methods=['DELETE'])
def delete_log(log_id):
    """
    Belirli bir işlem kaydını sil.
    """
    user = get_current_user()
    if not user:
        return error_response("Unauthorized", 401)

    log = AuditLog.query.get(log_id)
    if not log:
        return error_response("Log not found.", 404)

    db.session.delete(log)
    db.session.commit()

    return success_response(message="Log deleted successfully.")
