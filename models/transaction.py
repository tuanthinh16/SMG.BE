from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from pytz import timezone, utc
from common import convertTime
from config import db, SessionLocal  # SQLAlchemy instance and session factory
import graphene
from common.long import Long

# ORM Model
class TransactionModel(db.Model):
    __tablename__ = 'SMN_TRANSACTION'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    create_time = db.Column(db.BigInteger)
    creator = db.Column(db.String(50))
    modifier = db.Column(db.String(50))
    modify_time = db.Column(db.BigInteger)
    is_active = db.Column(db.Boolean, default=True)
    transaction_code = db.Column(db.String(50), nullable=False)
    transaction_name = db.Column(db.String(100))
    transaction_type_id = db.Column(db.BigInteger)
    transaction_time = db.Column(db.BigInteger)
    transaction_status = db.Column(db.String(50))
    transaction_description = db.Column(db.String(500))
    loginname = db.Column(db.String(50))
    is_cancel = db.Column(db.Boolean)
    is_confirmed = db.Column(db.Boolean)

# GraphQL Object Type
class Transaction(graphene.ObjectType):
    id = Long(name="ID")
    create_time = Long(name="CREATE_TIME")
    creator = graphene.String(name="CREATOR")
    modifier = graphene.String(name="MODIFIER")
    modify_time = Long(name="MODIFY_TIME")
    is_active = graphene.Boolean(name="IS_ACTIVE")
    transaction_code = graphene.String(name="TRANSACTION_CODE")
    transaction_name = graphene.String(name="TRANSACTION_NAME")
    transaction_type_id = Long(name="TRANSACTION_TYPE_ID")
    transaction_time = Long(name="TRANSACTION_TIME")
    transaction_status = graphene.String(name="TRANSACTION_STATUS")
    transaction_description = graphene.String(name="TRANSACTION_DESCRIPTION")
    loginname = graphene.String(name="LOGINNAME")
    is_cancel = graphene.Boolean(name="IS_CANCEL")
    is_confirmed = graphene.Boolean(name="IS_CONFIRMED")

# Query schema
class Query(graphene.ObjectType):
    transactions = graphene.List(Transaction)
    transaction_by_id = graphene.Field(Transaction, id=Long())
    transaction_by_code = graphene.Field(Transaction, transaction_code=graphene.String())

    def resolve_transactions(self, info):
        session = SessionLocal()
        try:
            return session.query(TransactionModel).all()
        finally:
            session.close()

    def resolve_transaction_by_id(self, info, id):
        session = SessionLocal()
        try:
            return session.query(TransactionModel).get(int(id))
        finally:
            session.close()

    def resolve_transaction_by_code(self, info, transaction_code):
        session = SessionLocal()
        try:
            return session.query(TransactionModel).filter_by(transaction_code=transaction_code).first()
        finally:
            session.close()

# Mutation schema
class CreateTransaction(graphene.Mutation):
    class Arguments:
        transaction_code = graphene.String()
        transaction_name = graphene.String()
        transaction_type_id = graphene.Int()
        transaction_status = graphene.String()
        transaction_description = graphene.String()
        loginname = graphene.String()
        is_cancel = graphene.Boolean()
        is_confirmed = graphene.Boolean()

    success = graphene.Boolean()
    transaction = graphene.Field(Transaction)

    @jwt_required()
    def mutate(self, info, transaction_code, transaction_name, transaction_type_id, transaction_status, transaction_description, loginname, is_cancel, is_confirmed):
        current_user = str(get_jwt_identity())
        create_time = convertTime.datetime_to_time_number(datetime.now(utc).astimezone(timezone('Asia/Bangkok')))

        new_transaction = TransactionModel(
            transaction_code=transaction_code,
            transaction_name=transaction_name,
            transaction_type_id=transaction_type_id,
            transaction_status=transaction_status,
            transaction_description=transaction_description,
            loginname=loginname,
            is_cancel=is_cancel,
            is_confirmed=is_confirmed,
            creator=current_user,
            create_time=create_time,
            is_active=True
        )

        session = SessionLocal()
        try:
            session.add(new_transaction)
            session.commit()
            transaction_id = new_transaction.id
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

        transaction = Transaction(
            id=transaction_id,
            transaction_code=transaction_code,
            transaction_name=transaction_name,
            transaction_type_id=transaction_type_id,
            transaction_status=transaction_status,
            transaction_description=transaction_description,
            loginname=loginname,
            is_cancel=is_cancel,
            is_confirmed=is_confirmed,
            creator=current_user,
            create_time=create_time,
            is_active=True
        )
        return CreateTransaction(success=True, transaction=transaction)

class UpdateTransaction(graphene.Mutation):
    class Arguments:
        id = graphene.Int()
        transaction_code = graphene.String()
        transaction_name = graphene.String()
        transaction_type_id = graphene.Int()
        transaction_status = graphene.String()
        transaction_description = graphene.String()
        loginname = graphene.String()
        is_cancel = graphene.Boolean()
        is_confirmed = graphene.Boolean()

    success = graphene.Boolean()
    transaction = graphene.Field(Transaction)

    @jwt_required()
    def mutate(self, info, id, transaction_code=None, transaction_name=None, transaction_type_id=None, transaction_status=None, transaction_description=None, loginname=None, is_cancel=None, is_confirmed=None):
        current_user = str(get_jwt_identity())
        modify_time = convertTime.datetime_to_time_number(datetime.now(utc).astimezone(timezone('Asia/Bangkok')))

        session = SessionLocal()
        try:
            transaction = session.query(TransactionModel).get(id)
            if transaction:
                if transaction_code:
                    transaction.transaction_code = transaction_code
                if transaction_name:
                    transaction.transaction_name = transaction_name
                if transaction_type_id:
                    transaction.transaction_type_id = transaction_type_id
                if transaction_status:
                    transaction.transaction_status = transaction_status
                if transaction_description:
                    transaction.transaction_description = transaction_description
                if loginname:
                    transaction.loginname = loginname
                if is_cancel is not None:
                    transaction.is_cancel = is_cancel
                if is_confirmed is not None:
                    transaction.is_confirmed = is_confirmed
                transaction.modifier = current_user
                transaction.modify_time = modify_time
                session.commit()
                return UpdateTransaction(success=True, transaction=transaction)
            else:
                return UpdateTransaction(success=False, transaction=None)
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

class DeleteTransaction(graphene.Mutation):
    class Arguments:
        id = graphene.Int()

    success = graphene.Boolean()

    @jwt_required()
    def mutate(self, info, id):
        session = SessionLocal()
        try:
            transaction = session.query(TransactionModel).get(id)
            if transaction:
                session.delete(transaction)
                session.commit()
                return DeleteTransaction(success=True)
            else:
                return DeleteTransaction(success=False)
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

class Mutation(graphene.ObjectType):
    create_transaction = CreateTransaction.Field()
    update_transaction = UpdateTransaction.Field()
    delete_transaction = DeleteTransaction.Field()

# Schema
schema = graphene.Schema(query=Query, mutation=Mutation)