from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from pytz import timezone, utc
from common import convertTime
from config import db, SessionLocal  # SQLAlchemy instance and session factory
import graphene
from common.long import Long

# ORM Model
class ReportDetailModel(db.Model):
    __tablename__ = 'SMN_REPORT_DETAIL'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    creator = db.Column(db.String(255))
    modifier = db.Column(db.String(255))
    is_active = db.Column(db.Boolean, default=True)
    report_type_code = db.Column(db.String(255), nullable=False)
    report_code = db.Column(db.String(255), nullable=False)
    report_json_filter = db.Column(db.String(4000))
    report_name = db.Column(db.String(500))
    report_detail_code = db.Column(db.String(500))
    output_file_name = db.Column(db.String(500))
    create_time = db.Column(db.BigInteger)
    modify_time = db.Column(db.BigInteger)

# GraphQL Object Type
class ReportDetail(graphene.ObjectType):
    id = Long(name="ID")
    creator = graphene.String(name="CREATOR")
    modifier = graphene.String(name="MODIFIER")
    is_active = graphene.Boolean(name="IS_ACTIVE")
    report_type_code = graphene.String(name="REPORT_TYPE_CODE")
    report_code = graphene.String(name="REPORT_CODE")
    report_json_filter = graphene.String(name="REPORT_JSON_FILTER")
    report_name = graphene.String(name="REPORT_NAME")
    report_detail_code = graphene.String(name="REPORT_DETAIL_CODE")
    output_file_name = graphene.String(name="OUTPUT_FILE_NAME")
    create_time = Long(name="CREATE_TIME")
    modify_time = Long(name="MODIFY_TIME")

# Query schema
class Query(graphene.ObjectType):
    report_details = graphene.List(ReportDetail)
    report_detail_by_id = graphene.Field(ReportDetail, id=Long())
    report_detail_by_code = graphene.Field(ReportDetail, report_code=graphene.String())

    def resolve_report_details(self, info):
        session = SessionLocal()
        try:
            return session.query(ReportDetailModel).all()
        finally:
            session.close()

    def resolve_report_detail_by_id(self, info, id):
        session = SessionLocal()
        try:
            return session.query(ReportDetailModel).get(int(id))
        finally:
            session.close()

    def resolve_report_detail_by_code(self, info, report_code):
        session = SessionLocal()
        try:
            return session.query(ReportDetailModel).filter_by(report_code=report_code).first()
        finally:
            session.close()

# Mutation schema
class CreateReportDetail(graphene.Mutation):
    class Arguments:
        creator = graphene.String()
        report_type_code = graphene.String()
        report_code = graphene.String()
        report_json_filter = graphene.String()
        report_name = graphene.String()
        report_detail_code = graphene.String()
        output_file_name = graphene.String()

    success = graphene.Boolean()
    report_detail = graphene.Field(ReportDetail)

    @jwt_required()
    def mutate(self, info, creator, report_type_code, report_code, report_json_filter, report_name, report_detail_code, output_file_name):
        current_user = str(get_jwt_identity())
        create_time = convertTime.datetime_to_time_number(datetime.now(utc).astimezone(timezone('Asia/Bangkok')))

        new_report_detail = ReportDetailModel(
            creator=creator,
            report_type_code=report_type_code,
            report_code=report_code,
            report_json_filter=report_json_filter,
            report_name=report_name,
            report_detail_code=report_detail_code,
            output_file_name=output_file_name,
            create_time=create_time,
            is_active=True
        )

        session = SessionLocal()
        try:
            session.add(new_report_detail)
            session.commit()
            report_detail_id = new_report_detail.id
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

        report_detail = ReportDetail(
            id=report_detail_id,
            creator=creator,
            report_type_code=report_type_code,
            report_code=report_code,
            report_json_filter=report_json_filter,
            report_name=report_name,
            report_detail_code=report_detail_code,
            output_file_name=output_file_name,
            create_time=create_time,
            is_active=True
        )
        return CreateReportDetail(success=True, report_detail=report_detail)

class UpdateReportDetail(graphene.Mutation):
    class Arguments:
        id = graphene.Int()
        report_type_code = graphene.String()
        report_code = graphene.String()
        report_json_filter = graphene.String()
        report_name = graphene.String()
        report_detail_code = graphene.String()
        output_file_name = graphene.String()
        modifier = graphene.String()

    success = graphene.Boolean()
    report_detail = graphene.Field(ReportDetail)

    @jwt_required()
    def mutate(self, info, id, report_type_code=None, report_code=None, report_json_filter=None, report_name=None, report_detail_code=None, output_file_name=None, modifier=None):
        current_user = str(get_jwt_identity())
        modify_time = convertTime.datetime_to_time_number(datetime.now(utc).astimezone(timezone('Asia/Bangkok')))

        session = SessionLocal()
        try:
            report_detail = session.query(ReportDetailModel).get(id)
            if report_detail:
                if report_type_code:
                    report_detail.report_type_code = report_type_code
                if report_code:
                    report_detail.report_code = report_code
                if report_json_filter:
                    report_detail.report_json_filter = report_json_filter
                if report_name:
                    report_detail.report_name = report_name
                if report_detail_code:
                    report_detail.report_detail_code = report_detail_code
                if output_file_name:
                    report_detail.output_file_name = output_file_name
                if modifier:
                    report_detail.modifier = modifier
                report_detail.modify_time = modify_time
                session.commit()
                return UpdateReportDetail(success=True, report_detail=report_detail)
            else:
                return UpdateReportDetail(success=False, report_detail=None)
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

class DeleteReportDetail(graphene.Mutation):
    class Arguments:
        id = graphene.Int()

    success = graphene.Boolean()

    @jwt_required()
    def mutate(self, info, id):
        session = SessionLocal()
        try:
            report_detail = session.query(ReportDetailModel).get(id)
            if report_detail:
                session.delete(report_detail)
                session.commit()
                return DeleteReportDetail(success=True)
            else:
                return DeleteReportDetail(success=False)
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

class Mutation(graphene.ObjectType):
    create_report_detail = CreateReportDetail.Field()
    update_report_detail = UpdateReportDetail.Field()
    delete_report_detail = DeleteReportDetail.Field()

# Schema
schema = graphene.Schema(query=Query, mutation=Mutation)