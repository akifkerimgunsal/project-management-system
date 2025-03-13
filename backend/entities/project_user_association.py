from datetime import datetime
from entities import db
from entities.enums.role_enum import Role

project_user_association = db.Table(
    'project_user_association',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('project_id', db.Integer, db.ForeignKey('projects.id'), primary_key=True),
    db.Column('role', db.Enum(Role), nullable=False, default=Role.VIEWER.name),
    db.Column('assigned_at', db.DateTime, default=datetime.utcnow, nullable=False)
)
