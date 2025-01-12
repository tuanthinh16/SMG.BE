from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from pytz import timezone, utc
from common import convertTime
from config import db, SessionLocal  # SQLAlchemy instance and session factory
import graphene
from common.long import Long

# ORM Model
class ExpMestClothesModel(db.Model):
    __tablename__ = 'SMN_EXP_MEST_CLOTHES'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    create_time = db.Column(db.BigInteger)
    creator = db.Column(db.String(50))
    modifier = db.Column(db.String(50))
    modify_time = db.Column(db.BigInteger)
    is_active = db.Column(db.Boolean, default=True)
    exp_mest_type_id = db.Column(db.String(50), nullable=False)
    exp_mest_stt_id = db.Column(db.String(50), nullable=False)
    exp_mest_code = db.Column(db.String(50), nullable=False)
    exp_mest_time = db.Column(db.BigInteger)
    exp_mest_status = db.Column(db.String(50))
    exp_mest_description = db.Column(db.String(500))
    clothes_type_id = db.Column(db.BigInteger)
    clothes_id = db.Column(db.BigInteger)
    loginname = db.Column(db.String(50))
    exp_time = db.Column(db.String(50))
    request_time = db.Column(db.String(50))
    request_loginname = db.Column(db.String(50))

# GraphQL Object Type
class ExpMestClothes(graphene.ObjectType):
    id = Long(name="ID")
    create_time = Long(name="CREATE_TIME")
    creator = graphene.String(name="CREATOR")
    modifier = graphene.String(name="MODIFIER")
    modify_time = Long(name="MODIFY_TIME")
    is_active = graphene.Boolean(name="IS_ACTIVE")
    exp_mest_type_id = graphene.String(name="EXP_MEST_TYPE_ID")
    exp_mest_stt_id = graphene.String(name="EXP_MEST_STT_ID")
    exp_mest_code = graphene.String(name="EXP_MEST_CODE")
    exp_mest_time = Long(name="EXP_MEST_TIME")
    exp_mest_status = graphene.String(name="EXP_MEST_STATUS")
    exp_mest_description = graphene.String(name="EXP_MEST_DESCRIPTION")
    clothes_type_id = Long(name="CLOTHES_TYPE_ID")
    clothes_id = Long(name="CLOTHES_ID")
    loginname = graphene.String(name="LOGINNAME")
    exp_time = graphene.String(name="EXP_TIME")
    request_time = graphene.String(name="REQUEST_TIME")
    request_loginname = graphene.String(name="REQUEST_LOGINNAME")

# Query schema
class Query(graphene.ObjectType):
    exp_mest_clothes = graphene.List(ExpMestClothes)
    exp_mest_clothes_by_id = graphene.Field(ExpMestClothes, id=Long())
    exp_mest_clothes_by_code = graphene.Field(ExpMestClothes, exp_mest_code=graphene.String())

    def resolve_exp_mest_clothes(self, info):
        session = SessionLocal()
        try:
            return session.query(ExpMestClothesModel).all()
        finally:
            session.close()

    def resolve_exp_mest_clothes_by_id(self, info, id):
        session = SessionLocal()
        try:
            return session.query(ExpMestClothesModel).get(int(id))
        finally:
            session.close()

    def resolve_exp_mest_clothes_by_code(self, info, exp_mest_code):
        session = SessionLocal()
        try:
            return session.query(ExpMestClothesModel).filter_by(exp_mest_code=exp_mest_code).first()
        finally:
            session.close()

# Mutation schema
class CreateExpMestClothes(graphene.Mutation):
    class Arguments:
        exp_mest_type_id = graphene.String()
        exp_mest_stt_id = graphene.String()
        exp_mest_code = graphene.String()
        exp_mest_time = graphene.Int()
        exp_mest_status = graphene.String()
        exp_mest_description = graphene.String()
        clothes_type_id = graphene.Int()
        clothes_id = graphene.Int()
        loginname = graphene.String()
        exp_time = graphene.String()
        request_time = graphene.String()
        request_loginname = graphene.String()

    success = graphene.Boolean()
    exp_mest_clothes = graphene.Field(ExpMestClothes)

    @jwt_required()
    def mutate(self, info, exp_mest_type_id, exp_mest_stt_id, exp_mest_code, exp_mest_time, exp_mest_status, exp_mest_description, clothes_type_id, clothes_id, loginname, exp_time, request_time, request_loginname):
        current_user = str(get_jwt_identity())
        create_time = convertTime.datetime_to_time_number(datetime.now(utc).astimezone(timezone('Asia/Bangkok')))

        new_exp_mest_clothes = ExpMestClothesModel(
            exp_mest_type_id=exp_mest_type_id,
            exp_mest_stt_id=exp_mest_stt_id,
            exp_mest_code=exp_mest_code,
            exp_mest_time=exp_mest_time,
            exp_mest_status=exp_mest_status,
            exp_mest_description=exp_mest_description,
            clothes_type_id=clothes_type_id,
            clothes_id=clothes_id,
            loginname=loginname,
            exp_time=exp_time,
            request_time=request_time,
            request_loginname=request_loginname,
            creator=current_user,
            create_time=create_time,
            is_active=True
        )

        session = SessionLocal()
        try:
            session.add(new_exp_mest_clothes)
            session.commit()
            exp_mest_clothes_id = new_exp_mest_clothes.id
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

        exp_mest_clothes = ExpMestClothes(
            id=exp_mest_clothes_id,
            exp_mest_type_id=exp_mest_type_id,
            exp_mest_stt_id=exp_mest_stt_id,
            exp_mest_code=exp_mest_code,
            exp_mest_time=exp_mest_time,
            exp_mest_status=exp_mest_status,
            exp_mest_description=exp_mest_description,
            clothes_type_id=clothes_type_id,
            clothes_id=clothes_id,
            loginname=loginname,
            exp_time=exp_time,
            request_time=request_time,
            request_loginname=request_loginname,
            creator=current_user,
            create_time=create_time,
            is_active=True
        )
        return CreateExpMestClothes(success=True, exp_mest_clothes=exp_mest_clothes)

class UpdateExpMestClothes(graphene.Mutation):
    class Arguments:
        id = graphene.Int()
        exp_mest_type_id = graphene.String()
        exp_mest_stt_id = graphene.String()
        exp_mest_code = graphene.String()
        exp_mest_time = graphene.Int()
        exp_mest_status = graphene.String()
        exp_mest_description = graphene.String()
        clothes_type_id = graphene.Int()
        clothes_id = graphene.Int()
        loginname = graphene.String()
        exp_time = graphene.String()
        request_time = graphene.String()
        request_loginname = graphene.String()

    success = graphene.Boolean()
    exp_mest_clothes = graphene.Field(ExpMestClothes)

    @jwt_required()
    def mutate(self, info, id, exp_mest_type_id=None, exp_mest_stt_id=None, exp_mest_code=None, exp_mest_time=None, exp_mest_status=None, exp_mest_description=None, clothes_type_id=None, clothes_id=None, loginname=None, exp_time=None, request_time=None, request_loginname=None):
        current_user = str(get_jwt_identity())
        modify_time = convertTime.datetime_to_time_number(datetime.now(utc).astimezone(timezone('Asia/Bangkok')))

        session = SessionLocal()
        try:
            exp_mest_clothes = session.query(ExpMestClothesModel).get(id)
            if exp_mest_clothes:
                if exp_mest_type_id:
                    exp_mest_clothes.exp_mest_type_id = exp_mest_type_id
                if exp_mest_stt_id:
                    exp_mest_clothes.exp_mest_stt_id = exp_mest_stt_id
                if exp_mest_code:
                    exp_mest_clothes.exp_mest_code = exp_mest_code
                if exp_mest_time is not None:
                    exp_mest_clothes.exp_mest_time = exp_mest_time
                if exp_mest_status:
                    exp_mest_clothes.exp_mest_status = exp_mest_status
                if exp_mest_description:
                    exp_mest_clothes.exp_mest_description = exp_mest_description
                if clothes_type_id is not None:
                    exp_mest_clothes.clothes_type_id = clothes_type_id
                if clothes_id is not None:
                    exp_mest_clothes.clothes_id = clothes_id
                if loginname:
                    exp_mest_clothes.loginname = loginname
                if exp_time:
                    exp_mest_clothes.exp_time = exp_time
                if request_time:
                    exp_mest_clothes.request_time = request_time
                if request_loginname:
                    exp_mest_clothes.request_loginname = request_loginname
                exp_mest_clothes.modifier = current_user
                exp_mest_clothes.modify_time = modify_time
                session.commit()
                return UpdateExpMestClothes(success=True, exp_mest_clothes=exp_mest_clothes)
            else:
                return UpdateExpMestClothes(success=False, exp_mest_clothes=None)
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

class DeleteExpMestClothes(graphene.Mutation):
    class Arguments:
        id = graphene.Int()

    success = graphene.Boolean()

    @jwt_required()
    def mutate(self, info, id):
        session = SessionLocal()
        try:
            exp_mest_clothes = session.query(ExpMestClothesModel).get(id)
            if exp_mest_clothes:
                session.delete(exp_mest_clothes)
                session.commit()
                return DeleteExpMestClothes(success=True)
            else:
                return DeleteExpMestClothes(success=False)
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

class Mutation(graphene.ObjectType):
    create_exp_mest_clothes = CreateExpMestClothes.Field()
    update_exp_mest_clothes = UpdateExpMestClothes.Field()
    delete_exp_mest_clothes = DeleteExpMestClothes.Field()

# Schema
schema = graphene.Schema(query=Query, mutation=Mutation)