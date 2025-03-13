from flask_sqlalchemy import SQLAlchemy

# Veritabanı entegrasyonu
db = SQLAlchemy()

# Modelleri içe aktarma
from entities.user import User
from entities.board import Board
from entities.project import Project
from entities.task import Task
from entities.refresh_token import RefreshToken
from entities.audit_log import AuditLog
from entities.board_user_association import board_user_association
from entities.project_user_association import project_user_association
from entities.task_user_association import task_user_association

# Dışa aktarılacak bileşenler
__all__ = [
    "db",
    "User",
    "Board",
    "Project",
    "Task",
    "RefreshToken",
    "AuditLog",
    "board_user_association",
    "project_user_association",
    "task_user_association",
]
