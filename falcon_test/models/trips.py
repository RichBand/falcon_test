import datetime
from marshmallow import Schema, fields, post_load
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String

BaseModel = declarative_base()


class TripModel(BaseModel):
    """
    for bikes_allowed and wheelchair_accessible:
        0 (or empty): Indicates that there is no accessibility information for the trip
        1: Indicates that the vehicle being used on this particular trip can accommodate at least one rider in a wheelchair
        2: Indicates that no riders in wheelchairs can be accommodated on this trip
    """
    __tablename__ = 'trip'

    trip_id = Column(Integer, index=True, nullable=False, unique=True)
    route_id = Column(Integer, ForeignKey('route.route_id'), index=True, nullable=False)
    service_id = Column(Integer, ForeignKey('calendar.service_id'), index=True, nullable=False)
    direction_id = Column(Integer, index=True)
    block_id = Column(String(255), index=True)
    shape_id = Column(String(255), index=True, nullable=True)
    trip_type = Column(String(255))
    trip_headsign = Column(String(255))
    trip_short_name = Column(String(255))
    bikes_allowed = Column(Integer, default=0)
    wheelchair_accessible = Column(Integer, default=0)

    id = Column(Integer, primary_key=True, autoincrement=True)
    created = Column(DateTime, default=datetime.datetime.now)
    modified = Column(DateTime, onupdate=datetime.datetime.now)
    deleted = Column(DateTime)


class TripSchema(Schema):
    class Meta:
        ordered = True
        strict = True

    trip_id = fields.Integer()
    route_id = fields.Integer()
    service_id = fields.Integer()
    direction_id = fields.Integer()
    block_id = fields.String()
    shape_id = fields.String()
    trip_type = fields.String()
    trip_headsign = fields.String()
    trip_short_name = fields.String()
    bikes_allowed = fields.Integer()
    wheelchair_accessible = fields.Integer()

    id = Column(Integer, primary_key=True, autoincrement=True)
    created = fields.DateTime(dump_only=True)
    modified = fields.DateTime(dump_only=True)
    deleted = fields.DateTime(dump_only=True)

    @post_load
    def create_model(self, data):
        return TripModel(**data)
