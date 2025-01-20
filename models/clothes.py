from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from pytz import timezone, utc
from common import convertTime
from config import db, SessionLocal  # SQLAlchemy instance and session factory
import graphene
from common.long import Long

# ORM Model
class ClothesModel(db.Model):
    __tablename__ = 'SMN_CLOTHES'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    create_time = db.Column(db.BigInteger)
    creator = db.Column(db.String(50))
    modifier = db.Column(db.String(50))
    modify_time = db.Column(db.BigInteger)
    is_active = db.Column(db.Boolean, default=True)
    clothes_code = db.Column(db.String(50), nullable=False)
    clothes_name = db.Column(db.String(100))
    clothes_type_id = db.Column(db.BigInteger)
    parent_id = db.Column(db.String(50))
    branch_name = db.Column(db.String(100))
    country_name = db.Column(db.String(100))
    clothes_size = db.Column(db.String(50))
    clothes_color = db.Column(db.String(50))
    amount = db.Column(db.Numeric(10, 2))
    price = db.Column(db.Numeric(10, 2))
    vat = db.Column(db.Numeric(10, 2))
    clothes_description = db.Column(db.String(500))
    clothes_image = db.Column(db.String(200))
    clothes_status = db.Column(db.String(50))
    imp_time = db.Column(db.String(50))
    username = db.Column(db.String(50))
    request_time = db.Column(db.String(50))
    request_status = db.Column(db.String(50))
    request_description = db.Column(db.String(500))

# GraphQL Object Type
class Clothes(graphene.ObjectType):
    id = Long(name="ID")
    create_time = Long(name="CREATE_TIME")
    creator = graphene.String(name="CREATOR")
    modifier = graphene.String(name="MODIFIER")
    modify_time = Long(name="MODIFY_TIME")
    is_active = graphene.Boolean(name="IS_ACTIVE")
    clothes_code = graphene.String(name="CLOTHES_CODE")
    clothes_name = graphene.String(name="CLOTHES_NAME")
    clothes_type_id = Long(name="CLOTHES_TYPE_ID")
    parent_id = graphene.String(name="PARENT_ID")
    branch_name = graphene.String(name="BRANCH_NAME")
    country_name = graphene.String(name="COUNTRY_NAME")
    clothes_size = graphene.String(name="CLOTHES_SIZE")
    clothes_color = graphene.String(name="CLOTHES_COLOR")
    amount = graphene.Float(name="AMOUNT")
    price = graphene.Float(name="PRICE")
    vat = graphene.Float(name="VAT")
    clothes_description = graphene.String(name="CLOTHES_DESCRIPTION")
    clothes_image = graphene.String(name="CLOTHES_IMAGE")
    clothes_status = graphene.String(name="CLOTHES_STATUS")
    imp_time = graphene.String(name="IMP_TIME")
    username = graphene.String(name="USERNAME")
    request_time = graphene.String(name="REQUEST_TIME")
    request_status = graphene.String(name="REQUEST_STATUS")
    request_description = graphene.String(name="REQUEST_DESCRIPTION")

# Query schema
class Query(graphene.ObjectType):
    clothes = graphene.List(Clothes)
    clothes_by_id = graphene.Field(Clothes, id=Long())
    clothes_by_code = graphene.Field(Clothes, clothes_code=graphene.String())

    def resolve_clothes(self, info):
        session = SessionLocal()
        try:
            return session.query(ClothesModel).all()
        finally:
            session.close()

    def resolve_clothes_by_id(self, info, id):
        session = SessionLocal()
        try:
            return session.query(ClothesModel).get(int(id))
        finally:
            session.close()

    def resolve_clothes_by_code(self, info, clothes_code):
        session = SessionLocal()
        try:
            return session.query(ClothesModel).filter_by(clothes_code=clothes_code).first()
        finally:
            session.close()

# Mutation schema
class CreateClothes(graphene.Mutation):
    class Arguments:
        clothes_code = graphene.String()
        clothes_name = graphene.String()
        clothes_type_id = graphene.Int()
        parent_id = graphene.String()
        branch_name = graphene.String()
        country_name = graphene.String()
        clothes_size = graphene.String()
        clothes_color = graphene.String()
        amount = graphene.Float()
        price = graphene.Float()
        vat = graphene.Float()
        clothes_description = graphene.String()
        clothes_image = graphene.String()
        clothes_status = graphene.String()
        imp_time = graphene.String()
        username = graphene.String()
        request_time = graphene.String()
        request_status = graphene.String()
        request_description = graphene.String()

    success = graphene.Boolean()
    clothes = graphene.Field(Clothes)

    @jwt_required()
    def mutate(self, info, **kwargs):
        current_user = str(get_jwt_identity())
        create_time = convertTime.datetime_to_time_number(datetime.now(utc).astimezone(timezone('Asia/Bangkok')))

        # Filter out None values
        kwargs = {k: v for k, v in kwargs.items() if v is not None}
        kwargs['creator'] = current_user
        kwargs['create_time'] = create_time
        kwargs['is_active'] = True

        new_clothes = ClothesModel(**kwargs)

        session = SessionLocal()
        try:
            session.add(new_clothes)
            session.commit()
            clothes_id = new_clothes.id
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

        clothes = Clothes(id=clothes_id, **kwargs)
        return CreateClothes(success=True, clothes=clothes)
    
class UpdateClothes(graphene.Mutation):
    class Arguments:
        id = graphene.Int()
        clothes_code = graphene.String()
        clothes_name = graphene.String()
        clothes_type_id = graphene.Int()
        parent_id = graphene.String()
        branch_name = graphene.String()
        country_name = graphene.String()
        clothes_size = graphene.String()
        clothes_color = graphene.String()
        amount = graphene.Float()
        price = graphene.Float()
        vat = graphene.Float()
        clothes_description = graphene.String()
        clothes_image = graphene.String()
        clothes_status = graphene.String()
        imp_time = graphene.String()
        username = graphene.String()
        request_time = graphene.String()
        request_status = graphene.String()
        request_description = graphene.String()

    success = graphene.Boolean()
    clothes = graphene.Field(Clothes)

    @jwt_required()
    def mutate(self, info, id, clothes_code=None, clothes_name=None, clothes_type_id=None, parent_id=None, branch_name=None, country_name=None, clothes_size=None, clothes_color=None, amount=None, price=None, vat=None, clothes_description=None, clothes_image=None, clothes_status=None, imp_time=None, username=None, request_time=None, request_status=None, request_description=None):
        current_user = str(get_jwt_identity())
        modify_time = convertTime.datetime_to_time_number(datetime.now(utc).astimezone(timezone('Asia/Bangkok')))

        session = SessionLocal()
        try:
            clothes = session.query(ClothesModel).get(id)
            if clothes:
                if clothes_code:
                    clothes.clothes_code = clothes_code
                if clothes_name:
                    clothes.clothes_name = clothes_name
                if clothes_type_id:
                    clothes.clothes_type_id = clothes_type_id
                if parent_id:
                    clothes.parent_id = parent_id
                if branch_name:
                    clothes.branch_name = branch_name
                if country_name:
                    clothes.country_name = country_name
                if clothes_size:
                    clothes.clothes_size = clothes_size
                if clothes_color:
                    clothes.clothes_color = clothes_color
                if amount is not None:
                    clothes.amount = amount
                if price is not None:
                    clothes.price = price
                if vat is not None:
                    clothes.vat = vat
                if clothes_description:
                    clothes.clothes_description = clothes_description
                if clothes_image:
                    clothes.clothes_image = clothes_image
                if clothes_status:
                    clothes.clothes_status = clothes_status
                if imp_time:
                    clothes.imp_time = imp_time
                if username:
                    clothes.username = username
                if request_time:
                    clothes.request_time = request_time
                if request_status:
                    clothes.request_status = request_status
                if request_description:
                    clothes.request_description = request_description
                clothes.modifier = current_user
                clothes.modify_time = modify_time
                session.commit()
                return UpdateClothes(success=True, clothes=clothes)
            else:
                return UpdateClothes(success=False, clothes=None)
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

class DeleteClothes(graphene.Mutation):
    class Arguments:
        id = graphene.Int()

    success = graphene.Boolean()

    @jwt_required()
    def mutate(self, info, id):
        session = SessionLocal()
        try:
            clothes = session.query(ClothesModel).get(id)
            if clothes:
                session.delete(clothes)
                session.commit()
                return DeleteClothes(success=True)
            else:
                return DeleteClothes(success=False)
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

class Mutation(graphene.ObjectType):
    create_clothes = CreateClothes.Field()
    update_clothes = UpdateClothes.Field()
    delete_clothes = DeleteClothes.Field()

# Schema
schema = graphene.Schema(query=Query, mutation=Mutation)