from datetime import datetime
from entities import db
from entities.enums.role_enum import Role

board_user_association = db.Table(
    'board_user_association',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('board_id', db.Integer, db.ForeignKey('boards.id'), primary_key=True),
    db.Column('role', db.Enum(Role), nullable=False, default=Role.VIEWER.name),
    db.Column('assigned_at', db.DateTime, default=datetime.utcnow, nullable=False)
)
