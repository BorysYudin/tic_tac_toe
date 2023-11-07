from marshmallow import Schema, fields

from app.extensions import ma


class UserSchemaMixin:
    """
    User fields that are similar to couple of Schemas
    """
    id = fields.Integer()
    username = fields.Str()
    age = fields.Integer()
    phone = fields.Str()
    is_deleted = fields.Boolean()
    rate = fields.Integer()
    position = fields.Integer()


class GetUserSchema(Schema, UserSchemaMixin):
    """
    User schema for data retrieval
    """
    pass


class ListUserSchema(Schema, UserSchemaMixin):
    """
    User schema for users list with additional link to entity field
    """
    url = ma.URLFor("user.get_user", values=dict(user_id="<id>"))


class UpdateUserSchema(Schema):
    """
    Schema for user update.
    """
    age = fields.Integer()
    phone = fields.Str()


class UserChartSchema(Schema):
    """
    Schema for user chart.
    """
    x = fields.Str()
    y = fields.Integer()
