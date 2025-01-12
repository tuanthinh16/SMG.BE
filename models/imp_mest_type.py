from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from pytz import timezone, utc
from common import convertTime
from config import db, SessionLocal  # SQLAlchemy instance and session factory
import graphene
from common.long import Long

# ORM Model
class ImpMestTypeModel(db.Model):
    __tablename__ = 'SMN_IMP_MEST_TYPE'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    create_time = db.Column(db.BigInteger)
    creator = db.Column(db.String(50))
    modifier = db.Column(db.String(50))
    modify_time = db.Column(db.BigInteger)
    is_active = db.Column(db.Boolean, default=True)
    imp_mest_type_code = db.Column(db.String(50), nullable=False)
    imp_mest_type_name = db.Column(db.String(100))

# GraphQL Object Type
class ImpMestType(graphene.ObjectType):
    id = Long(name="ID")
    create_time = Long(name="CREATE_TIME")
    creator = graphene.String(name="CREATOR")
    modifier = graphene.String(name="MODIFIER")
    modify_time = Long(name="MODIFY_TIME")
    is_active = graphene.Boolean(name="IS_ACTIVE")
    imp_mest_type_code = graphene.String(name="IMP_MEST_TYPE_CODE")
    imp_mest_type_name = graphene.String(name="IMP_MEST_TYPE_NAME")

# Query schema
class Query(graphene.ObjectType):
    imp_mest_types = graphene.List(ImpMestType)
    imp_mest_type_by_id = graphene.Field(ImpMestType, id=Long())
    imp_mest_type_by_code = graphene.Field(ImpMestType, imp_mest_type_code=graphene.String())

    def resolve_imp_mest_types(self, info):
        session = SessionLocal()
        try:
            return session.query(ImpMestTypeModel).all()
        finally:
            session.close()

    def resolve_imp_mest_type_by_id(self, info, id):
        session = SessionLocal()
        try:
            return session.query(ImpMestTypeModel).get(int(id))
        finally:
            session.close()

    def resolve_imp_mest_type_by_code(self, info, imp_mest_type_code):
        session = SessionLocal()
        try:
            return session.query(ImpMestTypeModel).filter_by(imp_mest_type_code=imp_mest_type_code).first()
        finally:
            session.close()

# Mutation schema
class CreateImpMestType(graphene.Mutation):
    class Arguments:
        imp_mest_type_code = graphene.String()
        imp_mest_type_name = graphene.String()

    success = graphene.Boolean()
    imp_mest_type = graphene.Field(ImpMestType)

    @jwt_required()
    def mutate(self, info, imp_mest_type_code, imp_mest_type_name):
        current_user = str(get_jwt_identity())
        create_time = convertTime.datetime_to_time_number(datetime.now(utc).astimezone(timezone('Asia/Bangkok')))

        new_imp_mest_type = ImpMestTypeModel(
            imp_mest_type_code=imp_mest_type_code,
            imp_mest_type_name=imp_mest_type_name,
            creator=current_user,
            create_time=create_time,
            is_active=True
        )

        session = SessionLocal()
        try:
            session.add(new_imp_mest_type)
            session.commit()
            imp_mest_type_id = new_imp_mest_type.id
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

        imp_mest_type = ImpMestType(
            id=imp_mest_type_id,
            imp_mest_type_code=imp_mest_type_code,
            imp_mest_type_name=imp_mest_type_name,
            creator=current_user,
            create_time=create_time,
            is_active=True
        )
        return CreateImpMestType(success=True, imp_mest_type=imp_mest_type)

class UpdateImpMestType(graphene.Mutation):
    class Arguments:
        id = graphene.Int()
        imp_mest_type_code = graphene.String()
        imp_mest_type_name = graphene.String()

    success = graphene.Boolean()
    imp_mest_type = graphene.Field(ImpMestType)

    @jwt_required()
    def mutate(self, info, id, imp_mest_type_code=None, imp_mest_type_name=None):
        current_user = str(get_jwt_identity())
        modify_time = convertTime.datetime_to_time_number(datetime.now(utc).astimezone(timezone('Asia/Bangkok')))

        session = SessionLocal()
        try:
            imp_mest_type = session.query(ImpMestTypeModel).get(id)
            if imp_mest_type:
                if imp_mest_type_code:
                    imp_mest_type.imp_mest_type_code = imp_mest_type_code
                if imp_mest_type_name:
                    imp_mest_type.imp_mest_type_name = imp_mest_type_name
                imp_mest_type.modifier = current_user
                imp_mest_type.modify_time = modify_time
                session.commit()
                return UpdateImpMestType(success=True, imp_mest_type=imp_mest_type)
            else:
                return UpdateImpMestType(success=False, imp_mest_type=None)
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

class DeleteImpMestType(graphene.Mutation):
    class Arguments:
        id = graphene.Int()

    success = graphene.Boolean()

    @jwt_required()
    def mutate(self, info, id):
        session = SessionLocal()
        try:
            imp_mest_type = session.query(ImpMestTypeModel).get(id)
            if imp_mest_type:
                session.delete(imp_mest_type)
                session.commit()
                return DeleteImpMestType(success=True)
            else:
                return DeleteImpMestType(success=False)
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

class Mutation(graphene.ObjectType):
    create_imp_mest_type = CreateImpMestType.Field()
    update_imp_mest_type = UpdateImpMestType.Field()
    delete_imp_mest_type = DeleteImpMestType.Field()

# Schema
schema = graphene.Schema(query=Query, mutation=Mutation)