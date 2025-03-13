from datetime import datetime
from entities import db
from entities.enums.role_enum import Role


task_user_association = db.Table(
    'task_user_association',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('task_id', db.Integer, db.ForeignKey('tasks.id'), primary_key=True),
    db.Column('role', db.Enum(Role), nullable=False, default=Role.VIEWER.value),
    db.Column('assigned_at', db.DateTime, default=datetime.utcnow, nullable=False)
)
