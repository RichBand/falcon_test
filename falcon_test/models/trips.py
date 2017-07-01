import datetime
from marshmallow import Schema, fields, post_dump
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, DateTime

BaseModel = declarative_base()


class Route(BaseModel):
    __tablename__ = 'route'

    id = Column(Integer, primary_key=True, autoincrement=True)
    route_id = Column(Integer, index=True, nullable=False, unique=True)
    route_short_name = Column(String(length=128), default='',)
    route_long_name = Column(String(length=128), nullable=False, unique=True)
    route_desc = Column(String(length=512), default='')
    route_color = Column(String(length=64), unique=True)
    route_type = Column(Integer, default=3)
    created = Column(DateTime, default=datetime.datetime.now)
    modified = Column(DateTime, onupdate=datetime.datetime.now)
    deleted = Column(DateTime)


class RouteSchema(Schema):
    class Meta:
        ordered = True
        strict = True

    route_id = fields.Integer()
    route_short_name = fields.String()
    route_long_name = fields.String()
    route_desc = fields.String()
    route_color = fields.String()
    route_type = fields.Integer()
    route_active = fields.Boolean()

    @post_dump
    def create_model(self, data):
        return Route(**data)


class Trip(BaseModel):
    __tablename__ = 'trip'

    id = Column(Integer, primary_key=True, autoincrement=True)

    created = DateTime()
    modified = DateTime()
    deleted = DateTime()


class Calendar(BaseModel):
    __tablename__ = 'calendar'

    id = Column(Integer, primary_key=True, autoincrement=True)
    service_id = Column(Integer, index=True, nullable=False)
    monday = Column(Boolean, default=False)
    tuesday = Column(Boolean, default=False)
    wednesday = Column(Boolean, default=False)
    thursday = Column(Boolean, default=False)
    friday = Column(Boolean, default=False)
    saturday = Column(Boolean, default=False)
    sunday = Column(Boolean, default=False)
    start_date = Column(DateTime, default=False)
    created = DateTime()
    modified = DateTime()
    deleted = DateTime()