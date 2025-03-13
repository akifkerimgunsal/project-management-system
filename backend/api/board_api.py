from flask import Blueprint, request
from entities import db
from entities.board import Board
from entities.board_user_association import board_user_association
from helpers.response_helpers import success_response, error_response
from helpers.auth_helpers import get_current_user
from helpers.authorization import authorize
from helpers.permissions import check_permission
from entities.enums.role_enum import Role
from entities.enums.board_status import BoardStatus

board_bp = Blueprint('board', __name__)

@board_bp.route('/', methods=['POST'])
def add_board():
    """
    Yeni bir pano oluşturur.
    """
    user = get_current_user()
    if not user:
        return error_response("Unauthorized", 401)

    data = request.get_json()
    name = data.get('name')
    description = data.get('description', '')
    status = data.get('status', BoardStatus.ACTIVE)

    if not name:
        return error_response("Board name is required.", 400)

    if status not in [status.value for status in BoardStatus]:
        return error_response(f"Invalid status value: {status}", 400)

    new_board = Board(
        name=name,
        description=description,
        status=status,
        created_by=user.id
    )
    db.session.add(new_board)
    db.session.commit()

    # Kullanıcıyı otomatik olarak Admin rolü ile panoya ekle
    db.session.execute(board_user_association.insert().values(
        user_id=user.id,
        board_id=new_board.id,
        role=Role.ADMIN.name
    ))
    db.session.commit()

    return success_response(data=new_board.to_dict(), message="Board created successfully.", status=201)

@board_bp.route('/', methods=['GET'])
def get_boards():
    """
    Kullanıcının erişebildiği tüm panoları döner.
    """
    user = get_current_user()
    if not user:
        return error_response("Unauthorized", 401)

    boards = db.session.query(Board).join(
        board_user_association,
        Board.id == board_user_association.c.board_id
    ).filter(
        board_user_association.c.user_id == user.id
    ).all()

    return success_response(data={"boards": [board.to_dict() for board in boards]}, message="Boards retrieved successfully.")


@board_bp.route('/<int:board_id>', methods=['PUT'])
def update_board(board_id):
    """
    Belirli bir panoyu günceller.
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
    board.name = data.get('name', board.name)
    board.description = data.get('description', board.description)
    board.status = data.get('status', board.status)

    if board.status not in [status.value for status in BoardStatus]:
        return error_response(f"Invalid status value: {board.status}", 400)

    db.session.commit()

    return success_response(data=board.to_dict(), message="Board updated successfully.")

@board_bp.route('/<int:board_id>', methods=['DELETE'])
def delete_board(board_id):
    """
    Belirli bir panoyu siler.
    """
    user = get_current_user()
    if not user:
        return error_response("Unauthorized", 401)

    board = Board.query.get(board_id)
    if not board:
        return error_response("Board not found.", 404)

    try:
        check_permission(user, board, [Role.ADMIN]) 
    except PermissionError as e:
        return error_response(str(e), 403)

    db.session.delete(board)
    db.session.commit()

    return success_response(message="Board deleted successfully.")

@board_bp.route('/<int:board_id>/add_user', methods=['POST'])
def add_user_to_board(board_id):
    """
    Belirli bir panoya kullanıcı ekler.
    """
    user = get_current_user()
    if not user:
        return error_response("Unauthorized", 401)

    board = Board.query.get(board_id)
    if not board:
        return error_response("Board not found.", 404)

    try:
        check_permission(user, board, [Role.ADMIN])
    except PermissionError as e:
        return error_response(str(e), 403)

    data = request.get_json()
    user_id = data.get('user_id')
    role = data.get('role', Role.VIEWER)

    if not user_id:
        return error_response("User ID is required.", 400)

    if role not in [role.value for role in Role]:
        return error_response(f"Invalid role value: {role}", 400)

    # Kullanıcıyı panoya ekle
    db.session.execute(board_user_association.insert().values(
        user_id=user_id,
        board_id=board.id,
        role=role
    ))
    db.session.commit()

    return success_response(message="User added to board successfully.")

@board_bp.route('/<int:board_id>/change_status', methods=['PATCH'])
def change_board_status(board_id):
    """
    Panonun durumunu günceller.
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
    new_status = data.get('status')

    if new_status not in [status.value for status in BoardStatus]:
        return error_response(f"Invalid status value: {new_status}", 400)

    board.status = new_status
    db.session.commit()

    return success_response(data=board.to_dict(), message="Board status updated successfully.")
