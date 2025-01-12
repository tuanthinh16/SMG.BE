from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from pytz import timezone, utc
from common import convertTime
from config import db, SessionLocal  # SQLAlchemy instance and session factory
import graphene
from common.long import Long

# ORM Model
class BillModel(db.Model):
    __tablename__ = 'SMN_BILL'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    create_time = db.Column(db.BigInteger)
    creator = db.Column(db.String(50))
    modifier = db.Column(db.String(50))
    modify_time = db.Column(db.BigInteger)
    is_active = db.Column(db.Boolean, default=True)
    bill_code = db.Column(db.String(50), nullable=False)
    bill_type_id = db.Column(db.BigInteger)
    bill_status = db.Column(db.BigInteger)
    bill_time = db.Column(db.BigInteger)
    bill_description = db.Column(db.String(500))
    loginname = db.Column(db.String(50))
    bill_id = db.Column(db.BigInteger)
    exp_mest_id = db.Column(db.BigInteger)
    imp_mest_id = db.Column(db.BigInteger)

# GraphQL Object Type
class Bill(graphene.ObjectType):
    id = Long(name="ID")
    create_time = Long(name="CREATE_TIME")
    creator = graphene.String(name="CREATOR")
    modifier = graphene.String(name="MODIFIER")
    modify_time = Long(name="MODIFY_TIME")
    is_active = graphene.Boolean(name="IS_ACTIVE")
    bill_code = graphene.String(name="BILL_CODE")
    bill_type_id = Long(name="BILL_TYPE_ID")
    bill_status = Long(name="BILL_STATUS")
    bill_time = Long(name="BILL_TIME")
    bill_description = graphene.String(name="BILL_DESCRIPTION")
    loginname = graphene.String(name="LOGINNAME")
    bill_id = Long(name="BILL_ID")
    exp_mest_id = Long(name="EXP_MEST_ID")
    imp_mest_id = Long(name="IMP_MEST_ID")

# Query schema
class Query(graphene.ObjectType):
    bills = graphene.List(Bill)
    bill_by_id = graphene.Field(Bill, id=Long())
    bill_by_code = graphene.Field(Bill, bill_code=graphene.String())

    def resolve_bills(self, info):
        session = SessionLocal()
        try:
            return session.query(BillModel).all()
        finally:
            session.close()

    def resolve_bill_by_id(self, info, id):
        session = SessionLocal()
        try:
            return session.query(BillModel).get(int(id))
        finally:
            session.close()

    def resolve_bill_by_code(self, info, bill_code):
        session = SessionLocal()
        try:
            return session.query(BillModel).filter_by(bill_code=bill_code).first()
        finally:
            session.close()

# Mutation schema
class CreateBill(graphene.Mutation):
    class Arguments:
        bill_code = graphene.String()
        bill_type_id = graphene.Int()
        bill_status = graphene.Int()
        bill_time = graphene.Int()
        bill_description = graphene.String()
        loginname = graphene.String()
        bill_id = graphene.Int()
        exp_mest_id = graphene.Int()
        imp_mest_id = graphene.Int()

    success = graphene.Boolean()
    bill = graphene.Field(Bill)

    @jwt_required()
    def mutate(self, info, bill_code, bill_type_id, bill_status, bill_time, bill_description, loginname, bill_id, exp_mest_id, imp_mest_id):
        current_user = str(get_jwt_identity())
        create_time = convertTime.datetime_to_time_number(datetime.now(utc).astimezone(timezone('Asia/Bangkok')))

        new_bill = BillModel(
            bill_code=bill_code,
            bill_type_id=bill_type_id,
            bill_status=bill_status,
            bill_time=bill_time,
            bill_description=bill_description,
            loginname=loginname,
            bill_id=bill_id,
            exp_mest_id=exp_mest_id,
            imp_mest_id=imp_mest_id,
            creator=current_user,
            create_time=create_time,
            is_active=True
        )

        session = SessionLocal()
        try:
            session.add(new_bill)
            session.commit()
            bill_id = new_bill.id
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

        bill = Bill(
            id=bill_id,
            bill_code=bill_code,
            bill_type_id=bill_type_id,
            bill_status=bill_status,
            bill_time=bill_time,
            bill_description=bill_description,
            loginname=loginname,
            bill_id=bill_id,
            exp_mest_id=exp_mest_id,
            imp_mest_id=imp_mest_id,
            creator=current_user,
            create_time=create_time,
            is_active=True
        )
        return CreateBill(success=True, bill=bill)

class UpdateBill(graphene.Mutation):
    class Arguments:
        id = graphene.Int()
        bill_code = graphene.String()
        bill_type_id = graphene.Int()
        bill_status = graphene.Int()
        bill_time = graphene.Int()
        bill_description = graphene.String()
        loginname = graphene.String()
        bill_id = graphene.Int()
        exp_mest_id = graphene.Int()
        imp_mest_id = graphene.Int()

    success = graphene.Boolean()
    bill = graphene.Field(Bill)

    @jwt_required()
    def mutate(self, info, id, bill_code=None, bill_type_id=None, bill_status=None, bill_time=None, bill_description=None, loginname=None, bill_id=None, exp_mest_id=None, imp_mest_id=None):
        current_user = str(get_jwt_identity())
        modify_time = convertTime.datetime_to_time_number(datetime.now(utc).astimezone(timezone('Asia/Bangkok')))

        session = SessionLocal()
        try:
            bill = session.query(BillModel).get(id)
            if bill:
                if bill_code:
                    bill.bill_code = bill_code
                if bill_type_id is not None:
                    bill.bill_type_id = bill_type_id
                if bill_status is not None:
                    bill.bill_status = bill_status
                if bill_time is not None:
                    bill.bill_time = bill_time
                if bill_description:
                    bill.bill_description = bill_description
                if loginname:
                    bill.loginname = loginname
                if bill_id is not None:
                    bill.bill_id = bill_id
                if exp_mest_id is not None:
                    bill.exp_mest_id = exp_mest_id
                if imp_mest_id is not None:
                    bill.imp_mest_id = imp_mest_id
                bill.modifier = current_user
                bill.modify_time = modify_time
                session.commit()
                return UpdateBill(success=True, bill=bill)
            else:
                return UpdateBill(success=False, bill=None)
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

class DeleteBill(graphene.Mutation):
    class Arguments:
        id = graphene.Int()

    success = graphene.Boolean()

    @jwt_required()
    def mutate(self, info, id):
        session = SessionLocal()
        try:
            bill = session.query(BillModel).get(id)
            if bill:
                session.delete(bill)
                session.commit()
                return DeleteBill(success=True)
            else:
                return DeleteBill(success=False)
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

class Mutation(graphene.ObjectType):
    create_bill = CreateBill.Field()
    update_bill = UpdateBill.Field()
    delete_bill = DeleteBill.Field()

# Schema
schema = graphene.Schema(query=Query, mutation=Mutation)