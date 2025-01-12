from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from pytz import timezone, utc
from common import convertTime
from config import db, SessionLocal  # SQLAlchemy instance and session factory
import graphene
from common.long import Long

# ORM Model
class ReportTypeModel(db.Model):
    __tablename__ = 'SMN_REPORT_TYPE'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    report_type_code = db.Column(db.String(255), nullable=False)
    report_type_name = db.Column(db.String(255), nullable=False)
    report_type_group_id = db.Column(db.BigInteger)
    create_time = db.Column(db.BigInteger, nullable=False)
    creator = db.Column(db.String(255), nullable=False)
    modifier = db.Column(db.String(255))
    modify_time = db.Column(db.BigInteger)
    is_active = db.Column(db.Boolean, default=True)

# GraphQL Object Type
class ReportType(graphene.ObjectType):
    id = Long(name="ID")
    report_type_code = graphene.String(name="REPORT_TYPE_CODE")
    report_type_name = graphene.String(name="REPORT_TYPE_NAME")
    report_type_group_id = Long(name="REPORT_TYPE_GROUP_ID")
    create_time = Long(name="CREATE_TIME")
    creator = graphene.String(name="CREATOR")
    modifier = graphene.String(name="MODIFIER")
    modify_time = Long(name="MODIFY_TIME")
    is_active = graphene.Boolean(name="IS_ACTIVE")

# Query schema
class Query(graphene.ObjectType):
    report_types = graphene.List(ReportType)
    report_type_by_id = graphene.Field(ReportType, id=Long())
    report_type_by_code = graphene.Field(ReportType, report_type_code=graphene.String())

    def resolve_report_types(self, info):
        session = SessionLocal()
        try:
            return session.query(ReportTypeModel).all()
        finally:
            session.close()

    def resolve_report_type_by_id(self, info, id):
        session = SessionLocal()
        try:
            return session.query(ReportTypeModel).get(int(id))
        finally:
            session.close()

    def resolve_report_type_by_code(self, info, report_type_code):
        session = SessionLocal()
        try:
            return session.query(ReportTypeModel).filter_by(report_type_code=report_type_code).first()
        finally:
            session.close()

# Mutation schema
class CreateReportType(graphene.Mutation):
    class Arguments:
        report_type_code = graphene.String()
        report_type_name = graphene.String()
        report_type_group_id = graphene.Int()
        creator = graphene.String()

    success = graphene.Boolean()
    report_type = graphene.Field(ReportType)

    @jwt_required()
    def mutate(self, info, report_type_code, report_type_name, report_type_group_id, creator):
        current_user = str(get_jwt_identity())
        create_time = convertTime.datetime_to_time_number(datetime.now(utc).astimezone(timezone('Asia/Bangkok')))

        new_report_type = ReportTypeModel(
            report_type_code=report_type_code,
            report_type_name=report_type_name,
            report_type_group_id=report_type_group_id,
            creator=creator,
            create_time=create_time,
            is_active=True
        )

        session = SessionLocal()
        try:
            session.add(new_report_type)
            session.commit()
            report_type_id = new_report_type.id
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

        report_type = ReportType(
            id=report_type_id,
            report_type_code=report_type_code,
            report_type_name=report_type_name,
            report_type_group_id=report_type_group_id,
            creator=creator,
            create_time=create_time,
            is_active=True
        )
        return CreateReportType(success=True, report_type=report_type)

class UpdateReportType(graphene.Mutation):
    class Arguments:
        id = graphene.Int()
        report_type_code = graphene.String()
        report_type_name = graphene.String()
        report_type_group_id = graphene.Int()
        modifier = graphene.String()

    success = graphene.Boolean()
    report_type = graphene.Field(ReportType)

    @jwt_required()
    def mutate(self, info, id, report_type_code=None, report_type_name=None, report_type_group_id=None, modifier=None):
        current_user = str(get_jwt_identity())
        modify_time = convertTime.datetime_to_time_number(datetime.now(utc).astimezone(timezone('Asia/Bangkok')))

        session = SessionLocal()
        try:
            report_type = session.query(ReportTypeModel).get(id)
            if report_type:
                if report_type_code:
                    report_type.report_type_code = report_type_code
                if report_type_name:
                    report_type.report_type_name = report_type_name
                if report_type_group_id is not None:
                    report_type.report_type_group_id = report_type_group_id
                if modifier:
                    report_type.modifier = modifier
                report_type.modify_time = modify_time
                session.commit()
                return UpdateReportType(success=True, report_type=report_type)
            else:
                return UpdateReportType(success=False, report_type=None)
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

class DeleteReportType(graphene.Mutation):
    class Arguments:
        id = graphene.Int()

    success = graphene.Boolean()

    @jwt_required()
    def mutate(self, info, id):
        session = SessionLocal()
        try:
            report_type = session.query(ReportTypeModel).get(id)
            if report_type:
                session.delete(report_type)
                session.commit()
                return DeleteReportType(success=True)
            else:
                return DeleteReportType(success=False)
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

class Mutation(graphene.ObjectType):
    create_report_type = CreateReportType.Field()
    update_report_type = UpdateReportType.Field()
    delete_report_type = DeleteReportType.Field()

# Schema
schema = graphene.Schema(query=Query, mutation=Mutation)