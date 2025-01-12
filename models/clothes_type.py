from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from pytz import timezone, utc
from common import convertTime
from config import db, SessionLocal  # SQLAlchemy instance and session factory
import graphene
from common.long import Long

# ORM Model
class ClothesTypeModel(db.Model):
    __tablename__ = 'SMN_CLOTHES_TYPE'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    clothes_type_code = db.Column(db.String(50), nullable=False)
    clothes_type_name = db.Column(db.String(100))
    parent_id = db.Column(db.String(50))
    branch_name = db.Column(db.String(100))
    country_name = db.Column(db.String(100))
    clothes_type_description = db.Column(db.String(500))
    clothes_type_image = db.Column(db.String(200))
    create_time = db.Column(db.BigInteger)
    creator = db.Column(db.String(50))
    modifier = db.Column(db.String(50))
    modify_time = db.Column(db.BigInteger)
    is_active = db.Column(db.Boolean, default=True)

# GraphQL Object Type
class ClothesType(graphene.ObjectType):
    id = Long(name="ID")
    clothes_type_code = graphene.String(name="CLOTHES_TYPE_CODE")
    clothes_type_name = graphene.String(name="CLOTHES_TYPE_NAME")
    parent_id = graphene.String(name="PARENT_ID")
    branch_name = graphene.String(name="BRANCH_NAME")
    country_name = graphene.String(name="COUNTRY_NAME")
    clothes_type_description = graphene.String(name="CLOTHES_TYPE_DESCRIPTION")
    clothes_type_image = graphene.String(name="CLOTHES_TYPE_IMAGE")
    create_time = Long(name="CREATE_TIME")
    creator = graphene.String(name="CREATOR")
    modifier = graphene.String(name="MODIFIER")
    modify_time = Long(name="MODIFY_TIME")
    is_active = graphene.Boolean(name="IS_ACTIVE")

# Query schema
class Query(graphene.ObjectType):
    clothes_types = graphene.List(ClothesType)
    clothes_type_by_id = graphene.Field(ClothesType, id=Long())
    clothes_type_by_code = graphene.Field(ClothesType, clothes_type_code=graphene.String())

    def resolve_clothes_types(self, info):
        session = SessionLocal()
        try:
            return session.query(ClothesTypeModel).all()
        finally:
            session.close()

    def resolve_clothes_type_by_id(self, info, id):
        session = SessionLocal()
        try:
            return session.query(ClothesTypeModel).get(int(id))
        finally:
            session.close()

    def resolve_clothes_type_by_code(self, info, clothes_type_code):
        session = SessionLocal()
        try:
            return session.query(ClothesTypeModel).filter_by(clothes_type_code=clothes_type_code).first()
        finally:
            session.close()

# Mutation schema
class CreateClothesType(graphene.Mutation):
    class Arguments:
        clothes_type_code = graphene.String()
        clothes_type_name = graphene.String()
        parent_id = graphene.String()
        branch_name = graphene.String()
        country_name = graphene.String()
        clothes_type_description = graphene.String()
        clothes_type_image = graphene.String()

    success = graphene.Boolean()
    clothes_type = graphene.Field(ClothesType)

    @jwt_required()
    def mutate(self, info, clothes_type_code, clothes_type_name, parent_id, branch_name, country_name, clothes_type_description, clothes_type_image):
        current_user = str(get_jwt_identity())
        create_time = convertTime.datetime_to_time_number(datetime.now(utc).astimezone(timezone('Asia/Bangkok')))

        new_clothes_type = ClothesTypeModel(
            clothes_type_code=clothes_type_code,
            clothes_type_name=clothes_type_name,
            parent_id=parent_id,
            branch_name=branch_name,
            country_name=country_name,
            clothes_type_description=clothes_type_description,
            clothes_type_image=clothes_type_image,
            creator=current_user,
            create_time=create_time,
            is_active=True
        )

        session = SessionLocal()
        try:
            session.add(new_clothes_type)
            session.commit()
            clothes_type_id = new_clothes_type.id
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

        clothes_type = ClothesType(
            id=clothes_type_id,
            clothes_type_code=clothes_type_code,
            clothes_type_name=clothes_type_name,
            parent_id=parent_id,
            branch_name=branch_name,
            country_name=country_name,
            clothes_type_description=clothes_type_description,
            clothes_type_image=clothes_type_image,
            creator=current_user,
            create_time=create_time,
            is_active=True
        )
        return CreateClothesType(success=True, clothes_type=clothes_type)

class UpdateClothesType(graphene.Mutation):
    class Arguments:
        id = graphene.Int()
        clothes_type_code = graphene.String()
        clothes_type_name = graphene.String()
        parent_id = graphene.String()
        branch_name = graphene.String()
        country_name = graphene.String()
        clothes_type_description = graphene.String()
        clothes_type_image = graphene.String()

    success = graphene.Boolean()
    clothes_type = graphene.Field(ClothesType)

    @jwt_required()
    def mutate(self, info, id, clothes_type_code=None, clothes_type_name=None, parent_id=None, branch_name=None, country_name=None, clothes_type_description=None, clothes_type_image=None):
        current_user = str(get_jwt_identity())
        modify_time = convertTime.datetime_to_time_number(datetime.now(utc).astimezone(timezone('Asia/Bangkok')))

        session = SessionLocal()
        try:
            clothes_type = session.query(ClothesTypeModel).get(id)
            if clothes_type:
                if clothes_type_code:
                    clothes_type.clothes_type_code = clothes_type_code
                if clothes_type_name:
                    clothes_type.clothes_type_name = clothes_type_name
                if parent_id:
                    clothes_type.parent_id = parent_id
                if branch_name:
                    clothes_type.branch_name = branch_name
                if country_name:
                    clothes_type.country_name = country_name
                if clothes_type_description:
                    clothes_type.clothes_type_description = clothes_type_description
                if clothes_type_image:
                    clothes_type.clothes_type_image = clothes_type_image
                clothes_type.modifier = current_user
                clothes_type.modify_time = modify_time
                session.commit()
                return UpdateClothesType(success=True, clothes_type=clothes_type)
            else:
                return UpdateClothesType(success=False, clothes_type=None)
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

class DeleteClothesType(graphene.Mutation):
    class Arguments:
        id = graphene.Int()

    success = graphene.Boolean()

    @jwt_required()
    def mutate(self, info, id):
        session = SessionLocal()
        try:
            clothes_type = session.query(ClothesTypeModel).get(id)
            if clothes_type:
                session.delete(clothes_type)
                session.commit()
                return DeleteClothesType(success=True)
            else:
                return DeleteClothesType(success=False)
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

class Mutation(graphene.ObjectType):
    create_clothes_type = CreateClothesType.Field()
    update_clothes_type = UpdateClothesType.Field()
    delete_clothes_type = DeleteClothesType.Field()

# Schema
schema = graphene.Schema(query=Query, mutation=Mutation)