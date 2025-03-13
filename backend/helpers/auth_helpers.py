import jwt
from flask import request, jsonify
from entities.user import User
from entities.enums.user_status import UserStatus
from entities import db
import os

SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")  # Güvenli anahtar

def get_current_user():
    """
    HTTP başlığındaki JWT'yi kontrol eder ve oturum açmış kullanıcıyı döner.
    """
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({"error": "Authorization header is missing"}), 401

    try:
        # Bearer token kontrolü
        token = auth_header.split(" ")[1]
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user_id = decoded_token.get("user_id")

        # Kullanıcıyı veritabanından getir
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": f"User not found with ID {user_id}"}), 404
        
        # Kullanıcı durumunu kontrol et
        if user.status != UserStatus.ACTIVE.value:
            return jsonify({"error": f"User status is {user.status}. Access denied."}), 403
        
        return user
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token has expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token"}), 401
