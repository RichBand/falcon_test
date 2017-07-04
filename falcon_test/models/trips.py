import datetime
from marshmallow import Schema, fields, post_load
from sqlalchemy.orm import relationship
from .base import BaseModel
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String


class TripModel(BaseModel):
    """
    for bikes_allowed and wheelchair_accessible:
        0 (or empty): Indicates that there is no accessibility information for the trip
        1: Indicates that the vehicle being used on this particular trip can accommodate at least one rider in a wheelchair
        2: Indicates that no riders in wheelchairs can be accommodated on this trip
    """
    __tablename__ = 'trip'

    id = Column(Integer, primary_key=True, autoincrement=True)
    route_id = Column(Integer, ForeignKey('route.id'), index=True, nullable=False)
    calendar_id = Column(Integer, ForeignKey('calendar.id'), index=True, nullable=False)
    direction_id = Column(Integer, index=True)
    block_id = Column(String(255), index=True)
    shape_id = Column(String(255), index=True, nullable=True)
    type = Column(String(255))
    headsign = Column(String(255))
    short_name = Column(String(255))
    bikes_allowed = Column(Integer, default=0)
    wheelchair_accessible = Column(Integer, default=0)

    created = Column(DateTime, default=datetime.datetime.now)
    modified = Column(DateTime, onupdate=datetime.datetime.now)
    deleted = Column(DateTime)

    route = relationship(
        'Route',
        primaryjoin='Trip.route_id==Route.id',
        foreign_keys='(Trip.route_id)',
        uselist=False, viewonly=True)

    stop_times = relationship(
        'stop_time',
        primaryjoin='trip.id==stop_time.trip_id',
        foreign_keys='(trip.id)',
        order_by='stop_time.sequence',
        uselist=True, viewonly=True)

    calendar = relationship(
        'calendar',
        primaryjoin='trip.calendar_id==calendar.id',
        foreign_keys='(trip.calendar_id)',
        uselist=True, viewonly=True)


class TripSchema(Schema):
    class Meta:
        ordered = True
        strict = True

    id = fields.Integer()
    route_id = fields.Integer()
    service_id = fields.Integer()
    direction_id = fields.Integer()
    block_id = fields.String()
    shape_id = fields.String()
    type = fields.String()
    headsign = fields.String()
    short_name = fields.String()
    bikes_allowed = fields.Integer()
    wheelchair_accessible = fields.Integer()

    created = fields.DateTime(dump_only=True)
    modified = fields.DateTime(dump_only=True)
    deleted = fields.DateTime(dump_only=True)

    @post_load
    def create_model(self, data):
        return TripModel(**data)
