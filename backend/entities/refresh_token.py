from datetime import datetime, timedelta
from entities import db

class RefreshToken(db.Model):
    __tablename__ = 'refresh_tokens'

    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(255), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    ip_address = db.Column(db.String(45), nullable=True)  # IP adresi desteği
    device_info = db.Column(db.String(255), nullable=True)  # Cihaz bilgisi
    expires_at = db.Column(db.DateTime, nullable=False)  # Geçerlilik süresi
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    user = db.relationship('User', backref=db.backref('refresh_tokens', lazy=True))

    def is_expired(self):
        """
        Checks if the token has expired.
        """
        return datetime.utcnow() > self.expires_at

    def to_dict(self):
        """
        Converts the token object to a dictionary.
        """
        return {
            "id": self.id,
            "token": self.token,
            "user_id": self.user_id,
            "ip_address": self.ip_address,
            "device_info": self.device_info,
            "expires_at": self.expires_at.isoformat(),
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
