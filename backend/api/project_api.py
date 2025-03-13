from flask import Blueprint, request
from entities import db
from entities.project import Project
from entities.board import Board
from entities.project_user_association import project_user_association
from helpers.response_helpers import success_response, error_response
from helpers.auth_helpers import get_current_user
from helpers.permissions import check_permission
from entities.enums.role_enum import Role
from entities.enums.project_status import ProjectStatus

project_bp = Blueprint('project', __name__)

@project_bp.route('/<int:board_id>', methods=['POST'])
def add_project(board_id):
    """
    Belirli bir panoya yeni bir proje ekler.
    """
    user = get_current_user()
    if not user:
        return error_response("Unauthorized", 401)

    board = Board.query.get(board_id)
    if not board:
        return error_response("Board not found.", 404)

    try:
        check_permission(user, board, [Role.ADMIN, Role.EDITOR])
    except PermissionError as e:
        return error_response(str(e), 403)

    data = request.get_json()
    name = data.get('name')
    description = data.get('description', '')
    status = data.get('status', ProjectStatus.ACTIVE.value)
    start_date = data.get('start_date')
    end_date = data.get('end_date')

    if not name:
        return error_response("Project name is required.", 400)

    new_project = Project(
        name=name,
        description=description,
        status=status,
        start_date=start_date,
        end_date=end_date,
        board_id=board_id,
        created_by=user.id
    )
    db.session.add(new_project)
    db.session.commit()

    # Kullanıcıyı otomatik olarak Admin rolü ile projeye ekle
    db.session.execute(project_user_association.insert().values(
        user_id=user.id,
        project_id=new_project.id,
        role=Role.ADMIN.name
    ))
    db.session.commit()

    return success_response(data=new_project.to_dict(), message="Project added successfully.", status=201)

@project_bp.route('/<int:project_id>', methods=['GET'])
def get_project(project_id):
    """
    Belirli bir projeyi döner.
    """
    user = get_current_user()
    if not user:
        return error_response("Unauthorized", 401)

    project = Project.query.get(project_id)
    if not project:
        return error_response("Project not found.", 404)

    try:
        # Sadece proje üzerinden kontrol
        check_permission(user, project, [Role.ADMIN, Role.EDITOR, Role.VIEWER])
    except PermissionError as e:
        return error_response(str(e), 403)

    return success_response(data=project.to_dict(), message="Project retrieved successfully.")


@project_bp.route('/<int:project_id>', methods=['PUT'])
def update_project(project_id):
    """
    Belirli bir projeyi günceller.
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
    project.name = data.get('name', project.name)
    project.description = data.get('description', project.description)
    project.status = data.get('status', project.status)
    project.start_date = data.get('start_date', project.start_date)
    project.end_date = data.get('end_date', project.end_date)

    db.session.commit()

    return success_response(data=project.to_dict(), message="Project updated successfully.")

@project_bp.route('/<int:project_id>', methods=['DELETE'])
def delete_project(project_id):
    """
    Belirli bir projeyi siler.
    """
    user = get_current_user()
    if not user:
        return error_response("Unauthorized", 401)

    project = Project.query.get(project_id)
    if not project:
        return error_response("Project not found.", 404)

    try:
        check_permission(user, project, [Role.ADMIN])
    except PermissionError as e:
        return error_response(str(e), 403)

    db.session.delete(project)
    db.session.commit()

    return success_response(message="Project deleted successfully.")

@project_bp.route('/<int:project_id>/add_user', methods=['POST'])
def add_user_to_project(project_id):
    """
    Belirli bir projeye kullanıcı ekler.
    """
    user = get_current_user()
    if not user:
        return error_response("Unauthorized", 401)

    project = Project.query.get(project_id)
    if not project:
        return error_response("Project not found.", 404)

    try:
        check_permission(user, project, [Role.ADMIN])
    except PermissionError as e:
        return error_response(str(e), 403)

    data = request.get_json()
    user_id = data.get('user_id')
    role = data.get('role', Role.VIEWER.name)

    if not user_id:
        return error_response("User ID is required.", 400)

    if role not in [role.value for role in Role]:
        return error_response(f"Invalid role value: {role}", 400)

    # Kullanıcıyı projeye ekle
    db.session.execute(project_user_association.insert().values(
        user_id=user_id,
        project_id=project.id,
        role=role
    ))
    db.session.commit()

    return success_response(message="User added to project successfully.")
