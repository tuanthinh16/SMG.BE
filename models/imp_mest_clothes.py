from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from pytz import timezone, utc
from common import convertTime
from config import db, SessionLocal  # SQLAlchemy instance and session factory
import graphene
from common.long import Long

# ORM Model
class ImpMestClothesModel(db.Model):
    __tablename__ = 'SMN_IMP_MEST_CLOTHES'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    create_time = db.Column(db.BigInteger)
    creator = db.Column(db.String(50))
    modifier = db.Column(db.String(50))
    modify_time = db.Column(db.BigInteger)
    is_active = db.Column(db.Boolean, default=True)
    imp_mest_type_id = db.Column(db.String(50), nullable=False)
    imp_mest_stt_id = db.Column(db.String(50), nullable=False)
    imp_mest_code = db.Column(db.String(50), nullable=False)
    imp_mest_time = db.Column(db.BigInteger)
    imp_mest_status = db.Column(db.String(50))
    imp_mest_description = db.Column(db.String(500))
    clothes_type_id = db.Column(db.BigInteger)
    clothes_id = db.Column(db.BigInteger)
    loginname = db.Column(db.String(50))
    imp_time = db.Column(db.String(50))
    request_time = db.Column(db.String(50))
    request_loginname = db.Column(db.String(50))

# GraphQL Object Type
class ImpMestClothes(graphene.ObjectType):
    id = Long(name="ID")
    create_time = Long(name="CREATE_TIME")
    creator = graphene.String(name="CREATOR")
    modifier = graphene.String(name="MODIFIER")
    modify_time = Long(name="MODIFY_TIME")
    is_active = graphene.Boolean(name="IS_ACTIVE")
    imp_mest_type_id = graphene.String(name="IMP_MEST_TYPE_ID")
    imp_mest_stt_id = graphene.String(name="IMP_MEST_STT_ID")
    imp_mest_code = graphene.String(name="IMP_MEST_CODE")
    imp_mest_time = Long(name="IMP_MEST_TIME")
    imp_mest_status = graphene.String(name="IMP_MEST_STATUS")
    imp_mest_description = graphene.String(name="IMP_MEST_DESCRIPTION")
    clothes_type_id = Long(name="CLOTHES_TYPE_ID")
    clothes_id = Long(name="CLOTHES_ID")
    loginname = graphene.String(name="LOGINNAME")
    imp_time = graphene.String(name="IMP_TIME")
    request_time = graphene.String(name="REQUEST_TIME")
    request_loginname = graphene.String(name="REQUEST_LOGINNAME")

# Query schema
class Query(graphene.ObjectType):
    imp_mest_clothes = graphene.List(ImpMestClothes)
    imp_mest_clothes_by_id = graphene.Field(ImpMestClothes, id=Long())
    imp_mest_clothes_by_code = graphene.Field(ImpMestClothes, imp_mest_code=graphene.String())

    def resolve_imp_mest_clothes(self, info):
        session = SessionLocal()
        try:
            return session.query(ImpMestClothesModel).all()
        finally:
            session.close()

    def resolve_imp_mest_clothes_by_id(self, info, id):
        session = SessionLocal()
        try:
            return session.query(ImpMestClothesModel).get(int(id))
        finally:
            session.close()

    def resolve_imp_mest_clothes_by_code(self, info, imp_mest_code):
        session = SessionLocal()
        try:
            return session.query(ImpMestClothesModel).filter_by(imp_mest_code=imp_mest_code).first()
        finally:
            session.close()

# Mutation schema
class CreateImpMestClothes(graphene.Mutation):
    class Arguments:
        imp_mest_type_id = graphene.String()
        imp_mest_stt_id = graphene.String()
        imp_mest_code = graphene.String()
        imp_mest_time = graphene.Int()
        imp_mest_status = graphene.String()
        imp_mest_description = graphene.String()
        clothes_type_id = graphene.Int()
        clothes_id = graphene.Int()
        loginname = graphene.String()
        imp_time = graphene.String()
        request_time = graphene.String()
        request_loginname = graphene.String()

    success = graphene.Boolean()
    imp_mest_clothes = graphene.Field(ImpMestClothes)

    @jwt_required()
    def mutate(self, info, imp_mest_type_id, imp_mest_stt_id, imp_mest_code, imp_mest_time, imp_mest_status, imp_mest_description, clothes_type_id, clothes_id, loginname, imp_time, request_time, request_loginname):
        current_user = str(get_jwt_identity())
        create_time = convertTime.datetime_to_time_number(datetime.now(utc).astimezone(timezone('Asia/Bangkok')))

        new_imp_mest_clothes = ImpMestClothesModel(
            imp_mest_type_id=imp_mest_type_id,
            imp_mest_stt_id=imp_mest_stt_id,
            imp_mest_code=imp_mest_code,
            imp_mest_time=imp_mest_time,
            imp_mest_status=imp_mest_status,
            imp_mest_description=imp_mest_description,
            clothes_type_id=clothes_type_id,
            clothes_id=clothes_id,
            loginname=loginname,
            imp_time=imp_time,
            request_time=request_time,
            request_loginname=request_loginname,
            creator=current_user,
            create_time=create_time,
            is_active=True
        )

        session = SessionLocal()
        try:
            session.add(new_imp_mest_clothes)
            session.commit()
            imp_mest_clothes_id = new_imp_mest_clothes.id
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

        imp_mest_clothes = ImpMestClothes(
            id=imp_mest_clothes_id,
            imp_mest_type_id=imp_mest_type_id,
            imp_mest_stt_id=imp_mest_stt_id,
            imp_mest_code=imp_mest_code,
            imp_mest_time=imp_mest_time,
            imp_mest_status=imp_mest_status,
            imp_mest_description=imp_mest_description,
            clothes_type_id=clothes_type_id,
            clothes_id=clothes_id,
            loginname=loginname,
            imp_time=imp_time,
            request_time=request_time,
            request_loginname=request_loginname,
            creator=current_user,
            create_time=create_time,
            is_active=True
        )
        return CreateImpMestClothes(success=True, imp_mest_clothes=imp_mest_clothes)

class UpdateImpMestClothes(graphene.Mutation):
    class Arguments:
        id = graphene.Int()
        imp_mest_type_id = graphene.String()
        imp_mest_stt_id = graphene.String()
        imp_mest_code = graphene.String()
        imp_mest_time = graphene.Int()
        imp_mest_status = graphene.String()
        imp_mest_description = graphene.String()
        clothes_type_id = graphene.Int()
        clothes_id = graphene.Int()
        loginname = graphene.String()
        imp_time = graphene.String()
        request_time = graphene.String()
        request_loginname = graphene.String()

    success = graphene.Boolean()
    imp_mest_clothes = graphene.Field(ImpMestClothes)

    @jwt_required()
    def mutate(self, info, id, imp_mest_type_id=None, imp_mest_stt_id=None, imp_mest_code=None, imp_mest_time=None, imp_mest_status=None, imp_mest_description=None, clothes_type_id=None, clothes_id=None, loginname=None, imp_time=None, request_time=None, request_loginname=None):
        current_user = str(get_jwt_identity())
        modify_time = convertTime.datetime_to_time_number(datetime.now(utc).astimezone(timezone('Asia/Bangkok')))

        session = SessionLocal()
        try:
            imp_mest_clothes = session.query(ImpMestClothesModel).get(id)
            if imp_mest_clothes:
                if imp_mest_type_id:
                    imp_mest_clothes.imp_mest_type_id = imp_mest_type_id
                if imp_mest_stt_id:
                    imp_mest_clothes.imp_mest_stt_id = imp_mest_stt_id
                if imp_mest_code:
                    imp_mest_clothes.imp_mest_code = imp_mest_code
                if imp_mest_time is not None:
                    imp_mest_clothes.imp_mest_time = imp_mest_time
                if imp_mest_status:
                    imp_mest_clothes.imp_mest_status = imp_mest_status
                if imp_mest_description:
                    imp_mest_clothes.imp_mest_description = imp_mest_description
                if clothes_type_id is not None:
                    imp_mest_clothes.clothes_type_id = clothes_type_id
                if clothes_id is not None:
                    imp_mest_clothes.clothes_id = clothes_id
                if loginname:
                    imp_mest_clothes.loginname = loginname
                if imp_time:
                    imp_mest_clothes.imp_time = imp_time
                if request_time:
                    imp_mest_clothes.request_time = request_time
                if request_loginname:
                    imp_mest_clothes.request_loginname = request_loginname
                imp_mest_clothes.modifier = current_user
                imp_mest_clothes.modify_time = modify_time
                session.commit()
                return UpdateImpMestClothes(success=True, imp_mest_clothes=imp_mest_clothes)
            else:
                return UpdateImpMestClothes(success=False, imp_mest_clothes=None)
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

class DeleteImpMestClothes(graphene.Mutation):
    class Arguments:
        id = graphene.Int()

    success = graphene.Boolean()

    @jwt_required()
    def mutate(self, info, id):
        session = SessionLocal()
        try:
            imp_mest_clothes = session.query(ImpMestClothesModel).get(id)
            if imp_mest_clothes:
                session.delete(imp_mest_clothes)
                session.commit()
                return DeleteImpMestClothes(success=True)
            else:
                return DeleteImpMestClothes(success=False)
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

class Mutation(graphene.ObjectType):
    create_imp_mest_clothes = CreateImpMestClothes.Field()
    update_imp_mest_clothes = UpdateImpMestClothes.Field()
    delete_imp_mest_clothes = DeleteImpMestClothes.Field()

# Schema
schema = graphene.Schema(query=Query, mutation=Mutation)