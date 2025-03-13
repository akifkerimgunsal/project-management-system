from datetime import datetime
from entities import db
from entities.enums.status import Status
from entities.enums.task_priority import TaskPriority


class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(50), default=Status.NOT_STARTED.value, nullable=False)
    priority = db.Column(db.String(50), default=TaskPriority.MEDIUM.value, nullable=False)
    description = db.Column(db.String(500), nullable=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    due_date = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    assignees = db.relationship('User', secondary='task_user_association', back_populates='tasks')

    def to_dict(self):
        """
        Converts the task object to a dictionary.
        """
        return {
            "id": self.id,
            "task": self.task,
            "status": self.status,
            "priority": self.priority,
            "description": self.description,
            "project_id": self.project_id,
            "created_by": self.created_by,
            "start_date": self.start_date.isoformat(),
            "due_date": self.due_date.isoformat(),
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "assignees": [
                {"id": user.id, "first_name": user.first_name, "last_name": user.last_name}
                for user in self.assignees
            ]
        }
