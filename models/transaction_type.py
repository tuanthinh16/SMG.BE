from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from pytz import timezone, utc
from common import convertTime
from config import db, SessionLocal  # SQLAlchemy instance and session factory
import graphene
from common.long import Long

# ORM Model
class TransactionTypeModel(db.Model):
    __tablename__ = 'SMN_TRANSACTION_TYPE'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    create_time = db.Column(db.BigInteger)
    creator = db.Column(db.String(50))
    modifier = db.Column(db.String(50))
    modify_time = db.Column(db.BigInteger)
    is_active = db.Column(db.Boolean, default=True)
    transaction_type_code = db.Column(db.String(50), nullable=False)
    transaction_type_name = db.Column(db.String(100))

# GraphQL Object Type
class TransactionType(graphene.ObjectType):
    id = Long(name="ID")
    create_time = Long(name="CREATE_TIME")
    creator = graphene.String(name="CREATOR")
    modifier = graphene.String(name="MODIFIER")
    modify_time = Long(name="MODIFY_TIME")
    is_active = graphene.Boolean(name="IS_ACTIVE")
    transaction_type_code = graphene.String(name="TRANSACTION_TYPE_CODE")
    transaction_type_name = graphene.String(name="TRANSACTION_TYPE_NAME")

# Query schema
class Query(graphene.ObjectType):
    transaction_types = graphene.List(TransactionType)
    transaction_type_by_id = graphene.Field(TransactionType, id=Long())
    transaction_type_by_code = graphene.Field(TransactionType, transaction_type_code=graphene.String())

    def resolve_transaction_types(self, info):
        session = SessionLocal()
        try:
            return session.query(TransactionTypeModel).all()
        finally:
            session.close()

    def resolve_transaction_type_by_id(self, info, id):
        session = SessionLocal()
        try:
            return session.query(TransactionTypeModel).get(int(id))
        finally:
            session.close()

    def resolve_transaction_type_by_code(self, info, transaction_type_code):
        session = SessionLocal()
        try:
            return session.query(TransactionTypeModel).filter_by(transaction_type_code=transaction_type_code).first()
        finally:
            session.close()

# Mutation schema
class CreateTransactionType(graphene.Mutation):
    class Arguments:
        transaction_type_code = graphene.String()
        transaction_type_name = graphene.String()

    success = graphene.Boolean()
    transaction_type = graphene.Field(TransactionType)

    @jwt_required()
    def mutate(self, info, transaction_type_code, transaction_type_name):
        current_user = str(get_jwt_identity())
        create_time = convertTime.datetime_to_time_number(datetime.now(utc).astimezone(timezone('Asia/Bangkok')))

        new_transaction_type = TransactionTypeModel(
            transaction_type_code=transaction_type_code,
            transaction_type_name=transaction_type_name,
            creator=current_user,
            create_time=create_time,
            is_active=True
        )

        session = SessionLocal()
        try:
            session.add(new_transaction_type)
            session.commit()
            transaction_type_id = new_transaction_type.id
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

        transaction_type = TransactionType(
            id=transaction_type_id,
            transaction_type_code=transaction_type_code,
            transaction_type_name=transaction_type_name,
            creator=current_user,
            create_time=create_time,
            is_active=True
        )
        return CreateTransactionType(success=True, transaction_type=transaction_type)

class UpdateTransactionType(graphene.Mutation):
    class Arguments:
        id = graphene.Int()
        transaction_type_code = graphene.String()
        transaction_type_name = graphene.String()

    success = graphene.Boolean()
    transaction_type = graphene.Field(TransactionType)

    @jwt_required()
    def mutate(self, info, id, transaction_type_code=None, transaction_type_name=None):
        current_user = str(get_jwt_identity())
        modify_time = convertTime.datetime_to_time_number(datetime.now(utc).astimezone(timezone('Asia/Bangkok')))

        session = SessionLocal()
        try:
            transaction_type = session.query(TransactionTypeModel).get(id)
            if transaction_type:
                if transaction_type_code:
                    transaction_type.transaction_type_code = transaction_type_code
                if transaction_type_name:
                    transaction_type.transaction_type_name = transaction_type_name
                transaction_type.modifier = current_user
                transaction_type.modify_time = modify_time
                session.commit()
                return UpdateTransactionType(success=True, transaction_type=transaction_type)
            else:
                return UpdateTransactionType(success=False, transaction_type=None)
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

class DeleteTransactionType(graphene.Mutation):
    class Arguments:
        id = graphene.Int()

    success = graphene.Boolean()

    @jwt_required()
    def mutate(self, info, id):
        session = SessionLocal()
        try:
            transaction_type = session.query(TransactionTypeModel).get(id)
            if transaction_type:
                session.delete(transaction_type)
                session.commit()
                return DeleteTransactionType(success=True)
            else:
                return DeleteTransactionType(success=False)
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

class Mutation(graphene.ObjectType):
    create_transaction_type = CreateTransactionType.Field()
    update_transaction_type = UpdateTransactionType.Field()
    delete_transaction_type = DeleteTransactionType.Field()

# Schema
schema = graphene.Schema(query=Query, mutation=Mutation)