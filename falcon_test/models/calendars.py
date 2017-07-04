import datetime
from marshmallow import Schema, fields, post_dump
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer
from .base import BaseModel


class CalendarModel(BaseModel):
    __tablename__ = 'calendar'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    trip_id = Column(Integer, ForeignKey('trip.id'), index=True, nullable=False)
    monday = Column(Boolean, default=False)
    tuesday = Column(Boolean, default=False)
    wednesday = Column(Boolean, default=False)
    thursday = Column(Boolean, default=False)
    friday = Column(Boolean, default=False)
    saturday = Column(Boolean, default=False)
    sunday = Column(Boolean, default=False)
    start_date = Column(DateTime, default=False)

    created = Column(DateTime, default=datetime.datetime.now)
    modified = Column(DateTime, onupdate=datetime.datetime.now)
    deleted = Column(DateTime)


class CalendarSchema(Schema):
    class Meta:
        ordered = True
        strict = True

    id = fields.Integer()
    trip_id = fields.Integer()
    monday = fields.Boolean()
    tuesday = fields.Boolean()
    wednesday = fields.Boolean()
    thursday = fields.Boolean()
    friday = fields.Boolean()
    saturday = fields.Boolean()
    sunday = fields.Boolean()
    start_date = fields.DateTime()
    created = fields.DateTime(dump_only=True)
    modified = fields.DateTime(dump_only=True)
    deleted = fields.DateTime(dump_only=True)

    @post_dump
    def create_model(self, data):
        return CalendarModel(**data)
