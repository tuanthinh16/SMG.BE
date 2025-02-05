import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import timedelta

# Cấu hình cơ sở dữ liệu PostgreSQL
DB_USER = "postgres"  # Tên người dùng PostgreSQL
DB_PASSWORD = "Thinh1637"  # Mật khẩu người dùng PostgreSQL
DB_HOST = "localhost"  # Địa chỉ máy chủ PostgreSQL
DB_PORT = "1521"  # Cổng mặc định của PostgreSQL
DB_NAME = "SMN_RS"  # Tên cơ sở dữ liệu PostgreSQL

# Cấu hình URI kết nối cho SQLAlchemy
SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Tạo engine và session factory cho SQLAlchemy
engine = create_engine(SQLALCHEMY_DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Cấu hình Flask SQLAlchemy (cho ORM tích hợp với Flask)
db = SQLAlchemy()

# Cấu hình JWT
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'thinhvippronghean')  # Chìa khóa bí mật JWT
JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=2)  # Thời gian sống của access token
JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)  # Thời gian sống của refresh token

#Cấu hình Cloudinary
CLOUD_NAME = "dwweabf16"
API_KEY= "723518173222341"
API_SECRET = "KMNHUvnxM7qGRMyNSVVJdC1lQS8"

# Hàm kết nối cơ sở dữ liệu PostgreSQL thông thường (không dùng SQLAlchemy ORM)
def get_oracle_connection():
    import psycopg2
    connection = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    return connection
