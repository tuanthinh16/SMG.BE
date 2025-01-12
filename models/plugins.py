import log
import graphene
from datetime import datetime
from pytz import timezone, utc
from common import convertTime
from common.long import Long
from config import db
from flask_jwt_extended import jwt_required, get_jwt_identity


# Plugin Model
class PluginModel(db.Model):
    __tablename__ = 'SMN_PLUGINS'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    create_time = db.Column(db.BigInteger, nullable=False)
    creator = db.Column(db.String(255), nullable=False)
    modifier = db.Column(db.String(255), nullable=True)
    modify_time = db.Column(db.BigInteger, nullable=True)
    plugin_name = db.Column(db.String(255), nullable=False)
    plugin_link = db.Column(db.String(255), nullable=True)
    is_active = db.Column(db.Boolean, nullable=False, default=False)
    plugin_group_id = db.Column(db.BigInteger, nullable=True)
    plugin_type_id = db.Column(db.Integer, nullable=True)
    icon = db.Column(db.String(255), nullable=True)

# GraphQL ObjectType for Plugin
class Plugins(graphene.ObjectType):
    id = Long(name="ID")
    create_time = Long(name="CREATE_TIME")
    creator = graphene.String(name="CREATOR")
    modifier = graphene.String(name="MODIFIER")
    modify_time = Long(name="MODIFY_TIME")
    plugin_name = graphene.String(name="PLUGIN_NAME")
    plugin_link = graphene.String(name="PLUGIN_LINK")
    is_active = graphene.Boolean(name="IS_ACTIVE")
    plugin_group_id = Long(name="PLUGIN_GROUP_ID")
    plugin_type_id = graphene.Int(name="PLUGIN_TYPE_ID")
    icon = graphene.String(name="ICON")

# Mutation to Create a Plugin
class CreatePlugin(graphene.Mutation):
    class Arguments:
        plugin_name = graphene.String(name="PLUGIN_NAME")
        plugin_link = graphene.String(name="PLUGIN_LINK")
        is_active = graphene.Boolean(name="IS_ACTIVE", default_value=False)
        plugin_group_id = Long(name="PLUGIN_GROUP_ID", default_value=None)
        plugin_type_id = graphene.Int(name="PLUGIN_TYPE_ID", default_value=None)
        icon = graphene.String(name="ICON", default_value=None)

    success = graphene.Boolean()
    plugin = graphene.Field(Plugins)

    @jwt_required()
    def mutate(self, info, plugin_name, plugin_link=None, is_active=False, plugin_group_id=None, plugin_type_id=None, icon=None):
        current_user = get_jwt_identity()
        try:
            create_time = convertTime.datetime_to_time_number(
                datetime.now(utc).astimezone(timezone('Asia/Bangkok'))
            )
            plugin = PluginModel(
                plugin_name=plugin_name,
                plugin_link=plugin_link,
                is_active=is_active,
                plugin_group_id=plugin_group_id,
                plugin_type_id=plugin_type_id,
                icon=icon,
                creator=current_user if current_user else "ADMIN",
                create_time=create_time
            )
            db.session.add(plugin)
            db.session.commit()
            return CreatePlugin(success=True, plugin=plugin)
        except Exception as ex:
            log.logger.exception("Error creating plugin")
            db.session.rollback()
            return CreatePlugin(success=False, plugin=None)

# Mutation to Delete a Plugin
class DeletePlugin(graphene.Mutation):
    class Arguments:
        id = Long()

    success = graphene.Boolean()

    @jwt_required()
    def mutate(self, info, id):
        try:
            plugin = PluginModel.query.get(id)
            if not plugin:
                log.logger.warning(f"Plugin with ID {id} not found.")
                return DeletePlugin(success=False)

            db.session.delete(plugin)
            db.session.commit()
            return DeletePlugin(success=True)
        except Exception as ex:
            log.logger.exception("Error deleting plugin")
            db.session.rollback()
            return DeletePlugin(success=False)
# Mutation to Update a Plugin
class UpdatePlugin(graphene.Mutation):
    class Arguments:
        id = Long()
        plugin_name = graphene.String(name="PLUGIN_NAME")
        plugin_link = graphene.String(name="PLUGIN_LINK")
        is_active = graphene.Boolean(name="IS_ACTIVE", default_value=False)
        plugin_group_id = Long(name="PLUGIN_GROUP_ID", default_value=None)
        plugin_type_id = graphene.Int(name="PLUGIN_TYPE_ID", default_value=None)
        icon = graphene.String(name="ICON", default_value=None)

    success = graphene.Boolean()
    plugin = graphene.Field(Plugins)

    @jwt_required()
    def mutate(self, info, id, plugin_name=None, plugin_link=None, is_active=False, plugin_group_id=None, plugin_type_id=None, icon=None):
        current_user = get_jwt_identity()
        try:
            plugin = PluginModel.query.get(id)
            if not plugin:
                log.logger.warning(f"Plugin with ID {id} not found.")
                return UpdatePlugin(success=False, plugin=None)

            # Update the plugin fields
            if plugin_name is not None:
                plugin.plugin_name = plugin_name
            if plugin_link is not None:
                plugin.plugin_link = plugin_link
            if is_active is not None:
                plugin.is_active = is_active
            if plugin_group_id is not None:
                plugin.plugin_group_id = plugin_group_id
            if plugin_type_id is not None:
                plugin.plugin_type_id = plugin_type_id
            if icon is not None:
                plugin.icon = icon

            # Update the modifier and modify time
            plugin.modifier = current_user if current_user else "ADMIN"
            plugin.modify_time = convertTime.datetime_to_time_number(
                datetime.now(utc).astimezone(timezone('Asia/Bangkok'))
            )

            db.session.commit()
            return UpdatePlugin(success=True, plugin=plugin)
        except Exception as ex:
            log.logger.exception("Error updating plugin")
            db.session.rollback()
            return UpdatePlugin(success=False, plugin=None)
# Query to Fetch Plugins
class Query(graphene.ObjectType):
    plugins = graphene.List(Plugins)
    plugin_by_id = graphene.Field(Plugins, id=Long())

    def resolve_plugins(self, info):
        try:
            plugins = PluginModel.query.all()
            return [
                Plugins(
                    id=plugin.id,
                    create_time=plugin.create_time,
                    creator=plugin.creator,
                    modifier=plugin.modifier,
                    modify_time=plugin.modify_time,
                    plugin_name=plugin.plugin_name,
                    plugin_link=plugin.plugin_link,
                    is_active=plugin.is_active,
                    plugin_group_id=plugin.plugin_group_id,
                    plugin_type_id=plugin.plugin_type_id,
                    icon=plugin.icon
                ) for plugin in plugins
            ]
        except Exception as ex:
            log.logger.exception("Error fetching plugins")
            return []

    def resolve_plugin_by_id(self, info, id):
        try:
            plugin = PluginModel.query.get(int(id))
            if plugin:
                return Plugins(
                    id=plugin.id,
                    create_time=plugin.create_time,
                    creator=plugin.creator,
                    modifier=plugin.modifier,
                    modify_time=plugin.modify_time,
                    plugin_name=plugin.plugin_name,
                    plugin_link=plugin.plugin_link,
                    is_active=plugin.is_active,
                    plugin_group_id=plugin.plugin_group_id,
                    plugin_type_id=plugin.plugin_type_id,
                    icon=plugin.icon
                )
            return None
        except Exception as ex:
            log.logger.exception("Error fetching plugin by ID")
            return None

# Mutation Schema
class Mutation(graphene.ObjectType):
    create_plugin = CreatePlugin.Field()
    delete_plugin = DeletePlugin.Field()
    update_plugin = UpdatePlugin.Field()

