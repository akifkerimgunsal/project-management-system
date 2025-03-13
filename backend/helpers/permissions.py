from entities.board_user_association import board_user_association
from entities.project_user_association import project_user_association
from entities.task_user_association import task_user_association
from entities.enums.role_enum import Role
from entities import db
from entities.board import Board
from entities.project import Project
from entities.task import Task

def check_permission(user, entity, required_roles):
    """
    Kullanıcının belirli bir entity (board, project, task) üzerindeki yetkisini kontrol eder.
    """
    role = None

    if isinstance(entity, Board):
        role = db.session.execute(
            db.select(board_user_association.c.role).where(
                (board_user_association.c.user_id == user.id) &
                (board_user_association.c.board_id == entity.id)
            )
        ).scalar()
    elif isinstance(entity, Project):
        role = db.session.execute(
            db.select(project_user_association.c.role).where(
                (project_user_association.c.user_id == user.id) &
                (project_user_association.c.project_id == entity.id)
            )
        ).scalar()

        print(f"Checking permissions for user_id={user.id}, project_id={entity.id}, found role={role}")
    elif isinstance(entity, Task):
        role = db.session.execute(
            db.select(task_user_association.c.role).where(
                (task_user_association.c.user_id == user.id) &
                (task_user_association.c.task_id == entity.id)
            )
        ).scalar()
    else:
        raise ValueError(f"Unsupported entity type: {type(entity).__name__}")

    if not role:
        raise PermissionError(f"Role not found for user {user.id} on entity {entity.id}.")

    try:
        role_enum = Role(role)
    except ValueError:
        raise PermissionError(f"Invalid role value in the database: {role}")

    if role_enum not in required_roles:
        raise PermissionError(
            f"User does not have the required role. Required: {[r.name for r in required_roles]}, Found: {role_enum.name}"
        )

    return True