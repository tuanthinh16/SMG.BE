from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from pytz import timezone, utc
from common import convertTime
from config import SessionLocal
import graphene
from common.long import Long

def generate_crud(model, graphql_type):
    class Query(graphene.ObjectType):
        items = graphene.List(graphql_type)
        item_by_id = graphene.Field(graphql_type, id=Long())
        item_by_field = graphene.Field(graphql_type, field_name=graphene.String(), field_value=graphene.String())

        def resolve_items(self, info):
            session = SessionLocal()
            try:
                return session.query(model).all()
            finally:
                session.close()

        def resolve_item_by_id(self, info, id):
            session = SessionLocal()
            try:
                return session.query(model).get(int(id))
            finally:
                session.close()

        def resolve_item_by_field(self, info, field_name, field_value):
            session = SessionLocal()
            try:
                return session.query(model).filter(getattr(model, field_name) == field_value).first()
            finally:
                session.close()

    class CreateItem(graphene.Mutation):
        class Arguments:
            input = graphene.Argument(graphene.InputObjectType)

        success = graphene.Boolean()
        item = graphene.Field(graphql_type)

        @jwt_required()
        def mutate(self, info, input):
            current_user = str(get_jwt_identity())
            create_time = convertTime.datetime_to_time_number(datetime.now(utc).astimezone(timezone('Asia/Bangkok')))

            new_item = model(
                **input,
                creator=current_user,
                create_time=create_time,
                is_active=True
            )

            session = SessionLocal()
            try:
                session.add(new_item)
                session.commit()
                item_id = new_item.id
            except Exception as e:
                session.rollback()
                raise e
            finally:
                session.close()

            item = graphql_type(
                id=item_id,
                **input,
                creator=current_user,
                create_time=create_time,
                is_active=True
            )
            return CreateItem(success=True, item=item)

    class UpdateItem(graphene.Mutation):
        class Arguments:
            id = graphene.Int()
            input = graphene.Argument(graphene.InputObjectType)

        success = graphene.Boolean()
        item = graphene.Field(graphql_type)

        @jwt_required()
        def mutate(self, info, id, input):
            current_user = str(get_jwt_identity())
            modify_time = convertTime.datetime_to_time_number(datetime.now(utc).astimezone(timezone('Asia/Bangkok')))

            session = SessionLocal()
            try:
                item = session.query(model).get(id)
                if item:
                    for key, value in input.items():
                        setattr(item, key, value)
                    item.modifier = current_user
                    item.modify_time = modify_time
                    session.commit()
                    return UpdateItem(success=True, item=item)
                else:
                    return UpdateItem(success=False, item=None)
            except Exception as e:
                session.rollback()
                raise e
            finally:
                session.close()

    class DeleteItem(graphene.Mutation):
        class Arguments:
            id = graphene.Int()

        success = graphene.Boolean()

        @jwt_required()
        def mutate(self, info, id):
            session = SessionLocal()
            try:
                item = session.query(model).get(id)
                if item:
                    session.delete(item)
                    session.commit()
                    return DeleteItem(success=True)
                else:
                    return DeleteItem(success=False)
            except Exception as e:
                session.rollback()
                raise e
            finally:
                session.close()

    class Mutation(graphene.ObjectType):
        create_item = CreateItem.Field()
        update_item = UpdateItem.Field()
        delete_item = DeleteItem.Field()

    return Query, Mutation