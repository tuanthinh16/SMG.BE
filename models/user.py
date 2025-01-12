from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from pytz import timezone, utc
from common import convertTime
from config import db, SessionLocal  # SQLAlchemy instance and session factory
import graphene
from common.long import Long

# ORM Model
class UserModel(db.Model):
    __tablename__ = 'SMN_USER'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    creator = db.Column(db.String(255))
    modifier = db.Column(db.String(255))
    is_active = db.Column(db.Boolean, default=True)
    username = db.Column(db.String(255), nullable=False, unique=True)
    loginname = db.Column(db.String(255), nullable=False, unique=True)
    fullname = db.Column(db.String(255))
    address = db.Column(db.String(255))
    phone = db.Column(db.String(50))
    email = db.Column(db.String(255))
    role = db.Column(db.String(255))
    create_time = db.Column(db.BigInteger)
    modify_time = db.Column(db.BigInteger)
    password = db.Column(db.String(255))

# GraphQL Object Type
class User(graphene.ObjectType):
    id = Long(name="ID")
    creator = graphene.String(name="CREATOR")
    modifier = graphene.String(name="MODIFIER")
    is_active = graphene.Boolean(name="IS_ACTIVE")
    username = graphene.String(name="USERNAME")
    loginname = graphene.String(name="LOGINNAME")
    fullname = graphene.String(name="FULLNAME")
    address = graphene.String(name="ADDRESS")
    phone = graphene.String(name="PHONE")
    email = graphene.String(name="EMAIL")
    role = graphene.String(name="ROLE")
    create_time = Long(name="CREATE_TIME")
    modify_time = Long(name="MODIFY_TIME")
    password = graphene.String(name="PASSWORD")

# Mutation: Tạo người dùng mới
class CreateUser(graphene.Mutation):
    class Arguments:
        username = graphene.String(name="USERNAME")
        loginname = graphene.String(name="LOGINNAME")
        fullname = graphene.String(name="FULLNAME")
        address = graphene.String(name="ADDRESS")
        phone = graphene.String(name="PHONE")
        email = graphene.String(name="EMAIL")
        role = graphene.String(name="ROLE")
        password = graphene.String(name="PASSWORD")

    success = graphene.Boolean()
    user = graphene.Field(User)

    @jwt_required()
    def mutate(self, info, username, loginname, fullname, address, phone, email, role, password):
        current_user = str(get_jwt_identity())

        create_time = convertTime.datetime_to_time_number(
            datetime.now(utc).astimezone(timezone('Asia/Bangkok'))
        )

        new_user = UserModel(
            username=username,
            loginname=loginname,
            fullname=fullname,
            address=address,
            phone=phone,
            email=email,
            role=role,
            password=password,
            creator=current_user or "ADMIN",
            create_time=create_time
        )

        session = SessionLocal()
        try:
            session.add(new_user)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

        return CreateUser(success=True, user=new_user)

# Mutation: Cập nhật người dùng
class UpdateUser(graphene.Mutation):
    class Arguments:
        id = Long()
        username = graphene.String(name="USERNAME")
        loginname = graphene.String(name="LOGINNAME")
        fullname = graphene.String(name="FULLNAME")
        address = graphene.String(name="ADDRESS")
        phone = graphene.String(name="PHONE")
        email = graphene.String(name="EMAIL")
        role = graphene.String(name="ROLE")
        password = graphene.String(name="PASSWORD")

    success = graphene.Boolean()
    user = graphene.Field(User)

    @jwt_required()
    def mutate(self, info, id, username=None, loginname=None, fullname=None, address=None, phone=None, email=None, role=None, password=None):
        current_user = get_jwt_identity()
        session = SessionLocal()

        try:
            user = session.query(UserModel).get(id)
            if not user:
                return UpdateUser(success=False, user=None)

            modify_time = convertTime.datetime_to_time_number(
                datetime.now(utc).astimezone(timezone('Asia/Bangkok'))
            )

            user.username = username or user.username
            user.loginname = loginname or user.loginname
            user.fullname = fullname or user.fullname
            user.address = address or user.address
            user.phone = phone or user.phone
            user.email = email or user.email
            user.role = role or user.role
            user.password = password or user.password
            user.modifier = current_user or "ADMIN"
            user.modify_time = modify_time

            session.commit()
            return UpdateUser(success=True, user=user)
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

# Mutation: Xóa người dùng
class DeleteUser(graphene.Mutation):
    class Arguments:
        id = Long()

    success = graphene.Boolean()

    @jwt_required()
    def mutate(self, info, id):
        session = SessionLocal()

        try:
            user = session.query(UserModel).get(id)
            if not user:
                return DeleteUser(success=False)

            session.delete(user)
            session.commit()
            return DeleteUser(success=True)
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

# Query: Lấy danh sách người dùng
class Query(graphene.ObjectType):
    users = graphene.List(User)
    user_by_id = graphene.Field(User, id=Long())
    user_by_username = graphene.Field(User, username=graphene.String())

    def resolve_users(self, info):
        session = SessionLocal()
        try:
            return session.query(UserModel).all()
        finally:
            session.close()

    def resolve_user_by_id(self, info, id):
        session = SessionLocal()
        try:
            # Ensure that 'id' is treated as an integer (assuming Long is serialized correctly)
            return session.query(UserModel).get(int(id))
        finally:
            session.close()
    def resolve_user_by_username(self, info, username):
        session = SessionLocal()
        try:
            return session.query(UserModel).filter_by(username=username).first()
        finally:
            session.close()

# Mutation schema
class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
    delete_user = DeleteUser.Field()

