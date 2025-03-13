from api.auth_api import auth_bp
from api.project_api import project_bp
from api.task_api import task_bp
from api.board_api import board_bp
from api.audit_log_api import audit_log_bp

def register_blueprints(app):
    """
    Tüm Blueprint'leri uygulamaya kaydeder.
    """
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(project_bp, url_prefix='/projects')
    app.register_blueprint(task_bp, url_prefix='/tasks')
    app.register_blueprint(board_bp, url_prefix='/boards')
    app.register_blueprint(audit_log_bp, url_prefix='/logs')
