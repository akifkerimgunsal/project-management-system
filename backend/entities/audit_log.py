from datetime import datetime
from entities import db
from entities.enums.entity_type import EntityType

class AuditLog(db.Model):
    __tablename__ = 'audit_logs'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    entity_id = db.Column(db.Integer, nullable=False)  # İlgili kaydın ID'si
    entity_type = db.Column(db.Enum(EntityType), nullable=False)  # İlgili model türü
    action = db.Column(db.String(50), nullable=False)  # Örn: "Create", "Update", "Delete"
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    details = db.Column(db.Text, nullable=True)  # Ek detaylar için

    # Relationships
    user = db.relationship('User', backref=db.backref('audit_logs', lazy=True))

    def to_dict(self):
        """
        Converts the audit log object to a dictionary.
        """
        return {
            "id": self.id,
            "user_id": self.user_id,
            "entity_id": self.entity_id,
            "entity_type": self.entity_type.value,
            "action": self.action,
            "timestamp": self.timestamp.isoformat(),
            "details": self.details
        }
