from datetime import datetime
from entities import db
from entities.enums.board_status import BoardStatus

class Board(db.Model):
    __tablename__ = 'boards'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    status = db.Column(db.String(50), default=BoardStatus.ACTIVE.value, nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    projects = db.relationship('Project', backref='board', lazy=True, cascade='all, delete-orphan')
    users = db.relationship('User', secondary='board_user_association', back_populates='boards')

    def to_dict(self):
        """
        Converts the board object to a dictionary.
        """
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "status": self.status,
            "created_by": self.created_by,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
