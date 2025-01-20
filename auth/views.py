from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from sqlalchemy.orm import Session
from config import SessionLocal
from models.user import UserModel as User
import log

auth_blueprint = Blueprint('auth', __name__)

# Đăng nhập và cấp token JWT
@auth_blueprint.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({"error": "Username and password are required"}), 400

    username = data['username']
    password = data['password']
    print(username, password)
    # Kiểm tra thông tin đăng nhập trong CSDL
    session: Session = SessionLocal()
    try:
        user = session.query(User).filter(User.username == username).first()
        if not user or user.password != password:  # Kiểm tra mật khẩu
            log.logger.warning(f"Login failed for username: {username}")
            return jsonify({"error": "Invalid credentials"}), 401

        # Tạo token JWT
        user_id = str(user.username)  # Lấy ID người dùng
        log.logger.info(f"Creating access token for user ID: {user_id}")
        access_token = create_access_token(identity=user_id)

        return jsonify(access_token=access_token)
    except Exception as e:
        log.logger.exception("Error during login"+str(e))
        return jsonify({"error": "Internal server error"}), 500
    finally:
        session.close()

# Kiểm tra token JWT
@auth_blueprint.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user_id = get_jwt_identity()  # Lấy ID người dùng từ token
    log.logger.debug(f"Current user ID from token: {current_user_id}")
    return jsonify(logged_in_as=current_user_id), 200
