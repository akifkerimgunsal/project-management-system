from flask import Blueprint, request
from werkzeug.security import check_password_hash, generate_password_hash
from entities import db
from entities.user import User
from entities.refresh_token import RefreshToken
from entities.enums.user_status import UserStatus
from helpers.response_helpers import success_response, error_response
from datetime import datetime, timedelta
import jwt
import os

# Ortam değişkenlerinden SECRET_KEY alınır
SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")

auth_bp = Blueprint('auth', __name__)

def generate_access_token(user_id, expires_in=1):
    """
    Kullanıcı için JWT access token üretir.
    """
    return jwt.encode({
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(hours=expires_in)
    }, SECRET_KEY, algorithm="HS256")

@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Yeni kullanıcı kaydı oluşturur.
    """
    data = request.get_json()
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    email = data.get('email')
    password = data.get('password')

    # Gerekli alanların kontrolü
    if not all([first_name, last_name, email, password]):
        return error_response("All fields are required.", status=400)

    # Kullanıcı e-posta kontrolü
    if User.query.filter_by(email=email).first():
        return error_response("Email already exists.", status=409)

    hashed_password = generate_password_hash(password)
    new_user = User(first_name=first_name, last_name=last_name, email=email, password_hash=hashed_password)

    db.session.add(new_user)
    db.session.commit()

    return success_response(message="User registered successfully.", status=201)

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Kullanıcı giriş işlemi.
    """
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    # Gerekli alanların kontrolü
    if not all([email, password]):
        return error_response("Email and password are required.", status=400)

    user = User.query.filter_by(email=email).first()

    # Kullanıcı doğrulama
    if not user or not user.check_password(password):
        return error_response("Invalid email or password.", status=401)

    if user.status != UserStatus.ACTIVE.value:
        return error_response(f"User is {user.status}. Access denied.", status=403)

    # Access ve refresh token oluşturma
    access_token = generate_access_token(user.id)
    refresh_token = RefreshToken(
        user_id=user.id,
        token=generate_access_token(user.id, expires_in=24 * 7),
        expires_at=datetime.utcnow() + timedelta(days=7)
    )

    user.update_last_login()
    db.session.add(refresh_token)
    db.session.commit()

    return success_response(data={
        "access_token": access_token,
        "refresh_token": refresh_token.token
    }, message="Login successful.")

@auth_bp.route('/refresh', methods=['POST'])
def refresh_token():
    """
    Kullanıcı için refresh token ile yeni bir access token oluşturur.
    """
    data = request.get_json()
    token = data.get('refresh_token')

    if not token:
        return error_response("Refresh token is required.", status=400)

    refresh_token_obj = RefreshToken.query.filter_by(token=token).first()

    # Refresh token doğrulama
    if not refresh_token_obj:
        return error_response("Invalid refresh token.", status=401)
    if refresh_token_obj.is_expired():
        return error_response("Refresh token has expired.", status=401)

    # Yeni access token oluşturma
    new_access_token = generate_access_token(refresh_token_obj.user_id)
    return success_response(data={"access_token": new_access_token}, message="Token refreshed successfully.")

@auth_bp.route('/logout', methods=['POST'])
def logout():
    """
    Kullanıcı çıkış işlemi.
    """
    data = request.get_json()
    token = data.get('refresh_token')

    if not token:
        return error_response("Refresh token is required.", status=400)

    refresh_token_obj = RefreshToken.query.filter_by(token=token).first()

    if not refresh_token_obj:
        return error_response("Invalid refresh token.", status=401)

    # Token veritabanından silinir
    db.session.delete(refresh_token_obj)
    db.session.commit()

    return success_response(message="Logout successful.")
