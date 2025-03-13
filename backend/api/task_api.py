from flask import Blueprint, request
from datetime import datetime, timedelta
from entities import db
from entities.task import Task
from entities.project import Project
from entities.user import User
from entities.task_user_association import task_user_association
from helpers.response_helpers import success_response, error_response
from helpers.auth_helpers import get_current_user
from helpers.permissions import check_permission
from entities.enums.role_enum import Role
from entities.enums.status import Status
from entities.enums.task_priority import TaskPriority

task_bp = Blueprint('task', __name__)

@task_bp.route('/<int:project_id>', methods=['POST'])
def add_task(project_id):
    """
    Belirli bir projeye yeni bir görev ekler.
    """
    user = get_current_user()
    if not user:
        return error_response("Unauthorized", 401)

    project = Project.query.get(project_id)
    if not project:
        return error_response("Project not found.", 404)

    try:
        check_permission(user, project, [Role.ADMIN, Role.EDITOR])
    except PermissionError as e:
        return error_response(str(e), 403)

    data = request.get_json()
    task = data.get('task')
    priority = data.get('priority', TaskPriority.MEDIUM.value)
    status = data.get('status', Status.NOT_STARTED.value)
    description = data.get('description', '')
    start_date = data.get('start_date')
    due_date = data.get('due_date')

    if not task:
        return error_response("Task name is required.", 400)

    if status not in [status.value for status in Status]:
        return error_response(f"Invalid status value: {status}", 400)

    if priority not in [priority.value for priority in TaskPriority]:
        return error_response(f"Invalid priority value: {priority}", 400)

    new_task = Task(
        task=task,
        priority=priority,
        status=status,
        description=description,
        start_date=datetime.fromisoformat(start_date) if start_date else None,
        due_date=datetime.fromisoformat(due_date) if due_date else None,
        project_id=project_id,
        created_by=user.id
    )
    db.session.add(new_task)
    db.session.commit()

    # Görevi ekleyen kullanıcıya Admin rolü atanır
    db.session.execute(task_user_association.insert().values(
        user_id=user.id,
        task_id=new_task.id,
        role=Role.ADMIN.name
    ))
    db.session.commit()

    return success_response(data=new_task.to_dict(), message="Task added successfully.", status=201)

@task_bp.route('/', methods=['GET'])
def get_all_tasks():
    """
    Kullanıcının atanmış olduğu tüm görevleri döner.
    """
    user = get_current_user()
    if not user:
        return error_response("Unauthorized", 401)

    # Kullanıcının atanmış olduğu tüm görevleri çek
    tasks = db.session.query(Task).join(
        task_user_association,
        Task.id == task_user_association.c.task_id
    ).filter(
        task_user_association.c.user_id == user.id
    ).all()

    # Görevleri listeye dönüştür
    task_list = [task.to_dict() for task in tasks]

    return success_response(data={"tasks": task_list}, message="User's assigned tasks retrieved successfully.")

@task_bp.route('/upcoming', methods=['GET'])
def get_upcoming_tasks():
    """
    Önümüzdeki 1 hafta içerisinde başlayacak görevleri döner.
    """
    user = get_current_user()
    if not user:
        return error_response("Unauthorized", 401)

    today = datetime.now().date()
    next_week = today + timedelta(days=7)

    # 1 hafta içerisinde başlayacak görevleri filtrele
    tasks = Task.query.filter(
        Task.start_date >= today,
        Task.start_date <= next_week
    ).all()

    # Görevleri listeye dönüştür
    task_list = [task.to_dict() for task in tasks]

    return success_response(data={"tasks": task_list}, message="Tasks starting within the next 7 days retrieved successfully.")


@task_bp.route('/<int:task_id>/add_user', methods=['POST'])
def add_user_to_task(task_id):
    """
    Bir göreve kullanıcı ekler.
    """
    user = get_current_user()
    if not user:
        return error_response("Unauthorized", 401)

    task = Task.query.get(task_id)
    if not task:
        return error_response("Task not found.", 404)

    try:
        check_permission(user, task.project, [Role.ADMIN])
    except PermissionError as e:
        return error_response(str(e), 403)

    data = request.get_json()
    user_id = data.get('user_id')
    role = data.get('role', Role.VIEWER.name)

    if not user_id:
        return error_response("User ID is required.", 400)

    if role not in [role.name for role in Role]:
        return error_response(f"Invalid role value: {role}", 400)

    # Kullanıcı göreve eklenir
    db.session.execute(task_user_association.insert().values(
        user_id=user_id,
        task_id=task.id,
        role=role
    ))
    db.session.commit()

    return success_response(message="User added to task successfully.")


@task_bp.route('/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """
    Belirli bir görevi günceller.
    """
    user = get_current_user()
    if not user:
        return error_response("Unauthorized", 401)

    task = Task.query.get(task_id)
    if not task:
        return error_response("Task not found.", 404)

    try:
        check_permission(user, task.project, [Role.ADMIN, Role.EDITOR])
    except PermissionError as e:
        return error_response(str(e), 403)

    data = request.get_json()
    task.task = data.get('task', task.task)
    task.priority = data.get('priority', task.priority)
    task.status = data.get('status', task.status)
    task.description = data.get('description', task.description)
    task.start_date = datetime.fromisoformat(data.get('start_date', task.start_date.isoformat()))
    task.due_date = datetime.fromisoformat(data.get('due_date', task.due_date.isoformat()))

    if task.status not in [status.value for status in Status]:
        return error_response(f"Invalid status value: {task.status}", 400)

    db.session.commit()

    return success_response(data=task.to_dict(), message="Task updated successfully.")

@task_bp.route('/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """
    Belirli bir görevi siler.
    """
    user = get_current_user()
    if not user:
        return error_response("Unauthorized", 401)

    task = Task.query.get(task_id)
    if not task:
        return error_response("Task not found.", 404)

    try:
        check_permission(user, task.project, [Role.ADMIN])
    except PermissionError as e:
        return error_response(str(e), 403)

    db.session.delete(task)
    db.session.commit()

    return success_response(message="Task deleted successfully.")
