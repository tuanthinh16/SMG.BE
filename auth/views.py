from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from sqlalchemy.orm import Session
from config import SessionLocal
from models.user import UserModel as User
import log

auth_blueprint = Blueprint('auth', __name__)

# Đăng nhập và cấp access token, refresh token
@auth_blueprint.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({"error": "Username and password are required"}), 400

    username = data['username']
    password = data['password']
    print(username, password)
    
    session: Session = SessionLocal()
    try:
        user = session.query(User).filter(User.username.ilike(username)).first()
        if not user or user.password != password:
            log.logger.warning(f"Login failed for username: {username}")
            return jsonify({"error": "Invalid credentials"}), 401

        # Tạo access token và refresh token
        user_id = str(user.username)
        user_role = str(user.role)
        log.logger.info(f"Creating access token for user ID: {user_id}")
        access_token = create_access_token(identity=user_id, additional_claims={"role": user_role})
        refresh_token = create_refresh_token(identity=user_id)

        return jsonify(access_token=access_token, refresh_token=refresh_token)
    except Exception as e:
        log.logger.exception("Error during login" + str(e))
        return jsonify({"error": "Internal server error"}), 500
    finally:
        session.close()


# Endpoint để cấp lại access token từ refresh token
@auth_blueprint.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    # Tạo lại access token mới từ refresh token
    current_user_id = get_jwt_identity()  # Lấy thông tin người dùng từ refresh token
    access_token = create_access_token(identity=current_user_id)
    
    log.logger.info(f"Created new access token for user ID: {current_user_id}")
    return jsonify(access_token=access_token), 200

# Kiểm tra token JWT
@auth_blueprint.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user_id = get_jwt_identity()  # Lấy ID người dùng từ token
    log.logger.debug(f"Current user ID from token: {current_user_id}")
    return jsonify(logged_in_as=current_user_id), 200
