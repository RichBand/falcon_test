import datetime
from marshmallow import Schema, fields, post_load
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String

BaseModel = declarative_base()


class RouteModel(BaseModel):
    __tablename__ = 'route'

    route_id = Column(Integer, index=True, nullable=False, unique=True)
    agency_id = Column(String(255), ForeignKey('agency.agency_id'), nullable=False)
    route_short_name = Column(String(length=128), default='',)
    route_long_name = Column(String(length=128), nullable=False, unique=True)
    route_desc = Column(String(length=512), default='')
    route_color = Column(String(length=64), unique=True)
    route_type = Column(Integer, default=3)

    id = Column(Integer, primary_key=True, autoincrement=True)
    created = Column(DateTime, default=datetime.datetime.now)
    modified = Column(DateTime, onupdate=datetime.datetime.now)
    deleted = Column(DateTime)


class RouteSchema(Schema):
    class Meta:
        ordered = True
        strict = True

    route_id = fields.Integer()
    agency_id = fields.String()
    route_short_name = fields.String()
    route_long_name = fields.String()
    route_desc = fields.String()
    route_color = fields.String()
    route_type = fields.Integer()
    route_active = fields.Boolean()

    id = fields.Integer(dump_only=True)
    created = fields.DateTime(dump_only=True)
    modified = fields.DateTime(dump_only=True)
    deleted = fields.DateTime(dump_only=True)

    @post_load
    def create_model(self, data):
        return RouteModel(**data)
