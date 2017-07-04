import datetime
from marshmallow import Schema, fields, post_load
from sqlalchemy.orm import relationship
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from .base import BaseModel


class RouteModel(BaseModel):
    __tablename__ = 'route'

    id = Column(Integer, primary_key=True, nullable=False, index=True)
    agency_id = Column(String(255), ForeignKey('agency.id'), nullable=False)
    short_name = Column(String(length=128), default='',)
    long_name = Column(String(length=128), nullable=False, unique=True)
    desc = Column(String(length=512), default='')
    color = Column(String(length=64), unique=True)
    type = Column(Integer, default=3)

    created = Column(DateTime, default=datetime.datetime.now)
    modified = Column(DateTime, onupdate=datetime.datetime.now)
    deleted = Column(DateTime)

    trips = relationship(
        'trip',
        primaryjoin='route.id==trip.route_id',
        foreign_keys='(route.id)',
        uselist=True, viewonly=True)


class RouteSchema(Schema):
    class Meta:
        ordered = True
        strict = True

    id = fields.Integer()
    agency_id = fields.String()
    short_name = fields.String()
    long_name = fields.String()
    desc = fields.String()
    color = fields.String()
    type = fields.Integer()
    active = fields.Boolean()

    created = fields.DateTime(dump_only=True)
    modified = fields.DateTime(dump_only=True)
    deleted = fields.DateTime(dump_only=True)

    @post_load
    def create_model(self, data):
        return RouteModel(**data)
