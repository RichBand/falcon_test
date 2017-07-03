import datetime
from marshmallow import Schema, fields, post_dump
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, DateTime, ForeignKey, Integer, Numeric, String

BaseModel = declarative_base()


class StopTimeModel(BaseModel):
    """
    pickup_type:
        0: Regularly scheduled pickup
        1: No pickup available
        2: Must phone agency to arrange pickup
        3: Must coordinate with driver to arrange pickup
    drop_off_type:
        0: Regularly scheduled drop off
        1: No drop off available
        2: Must phone agency to arrange drop off
        3: Must coordinate with driver to arrange drop off
    timepoint
        empty: Times are considered exact.
        0: Times are considered approximate.
        1: Times are considered exact.
    """
    __tablename__ = 'stop_times'

    trip_id = Column(Integer, ForeignKey('trip.id'), primary_key=True, index=True, nullable=False)
    stop_id = Column(Integer, ForeignKey('stop.id'), index=True, nullable=False)
    sequence = Column(Integer, primary_key=True, nullable=False)
    arrival_time = Column(String(9))
    departure_time = Column(String(9), index=True)
    headsign = Column(String(255))
    pickup_type = Column(Integer, default=0)
    drop_off_type = Column(Integer, default=0)
    shape_dist_traveled = Column(Numeric(20, 10))
    timepoint = Column(Integer, default=0)

    created = Column(DateTime, default=datetime.datetime.now)
    modified = Column(DateTime, onupdate=datetime.datetime.now)
    deleted = Column(DateTime)

    stop = relationship(
        'stop',
        primaryjoin='stop.id==stop_time.stop_id',
        foreign_keys='(stop_time.stop_id)',
        uselist=False, viewonly=True)

    trip = relationship(
        'trip',
        primaryjoin='trip.id==stop_time.trip_id',
        foreign_keys='(stop_time.trip_id)',
        uselist=False, viewonly=True)


class StopTimeSchema(Schema):
    class Meta:
        ordered = True
        strict = True

    trip_id = fields.Integer()
    stop_id = fields.Integer()
    sequence = fields.Integer()
    arrival_time = fields.String()
    departure_time = fields.String()
    headsign = fields.String()
    pickup_type = fields.Integer()
    drop_off_type = fields.Integer()
    shape_dist_traveled = fields.Column(Numeric(20, 10))
    timepoint = fields.Integer()

    created = fields.DateTime(dump_only=True)
    modified = fields.DateTime(dump_only=True)
    deleted = fields.DateTime(dump_only=True)

    @post_dump
    def create_model(self, data):
        return StopTimeModel(**data)
