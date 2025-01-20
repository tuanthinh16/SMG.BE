import log
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_graphql import GraphQLView
from flask_jwt_extended import JWTManager
from schema import schema
from auth.views import auth_blueprint
from config import db, SessionLocal, engine, JWT_SECRET_KEY,SQLALCHEMY_DATABASE_URI,CLOUD_NAME,API_KEY,API_SECRET
import cloudinary
import cloudinary.uploader

app = Flask(__name__)
cors = CORS(app, resources={
    r"/api/*": {"origins": "*"},  # Cho phép tất cả các domain truy cập API
    r"/auth/login": {"origins": "*"}  # Cấu hình CORS cho /auth/login
})
# Cấu hình Flask-JWT-Extended
app.config['JWT_SECRET_KEY'] = JWT_SECRET_KEY  # Chìa khóa bí mật JWT lấy từ config
# Cấu hình Cloudinary
cloudinary.config(
    cloud_name=CLOUD_NAME,
    api_key=API_KEY,
    api_secret=API_SECRET
)

jwt = JWTManager(app)

# Cấu hình Flask-SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

# Tạo engine và session factory cho SQLAlchemy
db.init_app(app)  # Kết nối ứng dụng Flask với SQLAlchemy

# @app.before_request
# def create_tables():
#     # db.drop_all()
#     db.create_all()

# Đăng ký Blueprint cho Auth
app.register_blueprint(auth_blueprint, url_prefix='/auth')

# Cấu hình URL cho GraphQL
app.add_url_rule('/api/v1/', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True))

# Cấu hình logging
@app.before_request
def log_request():
    log.logger.info(f"Request Method: {request.method}")
    log.logger.info(f"Request URL: {request.url}")
    log.logger.info(f"Request Headers: {request.headers}")
    log.logger.info(f"Request Data: {request.get_data(as_text=True)}")  # Log data nếu có
#api nhận graphql
@app.route('/api/v1/', methods=['POST'])
def graphql_server():
    data = request.get_json()  # Nhận dữ liệu JSON từ POST request
    if data is None:
        return jsonify({"error": "No JSON payload"}), 400
    
    # Tạo GraphQLView và thực hiện truy vấn
    view = GraphQLView.as_view('graphql', schema=schema, graphiql=False)
    return view()
#Upload ảnh
@app.route('/api/v1/upload', methods=['POST'])
def Process_Upload():
    file = request.files['file'] 
    type = request.form['type']
    try:
        folder_name = "SMG/"+type
        upload_result = cloudinary.uploader.upload(file, folder=folder_name)
        return jsonify({"url": upload_result['secure_url']})  # Trả về URL của ảnh
    except Exception as e:
        return jsonify({"error": str(e)}), 500
#Upload nhiều ảnh
@app.route('/api/v1/upload-multiple', methods=['POST'])
def Process_Upload_Multiple():
    files = request.files.getlist('files')  # Lấy danh sách file từ request
    type = request.form['type']  # Lấy type từ form data

    if not files:
        return jsonify({"error": "No files uploaded"}), 400

    urls = []
    try:
        folder_name = f"SMG/{type}"  
        for file in files:
            upload_result = cloudinary.uploader.upload(file, folder=folder_name)
            urls.append(upload_result['secure_url']) 
        return jsonify({"urls": urls})  
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
    app.config["DEBUG"] = True
    app.testing = True
    app.run(debug=True)
    
