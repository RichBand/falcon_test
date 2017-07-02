import datetime
from marshmallow import Schema, fields, post_dump
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

    trip_id = Column(Integer, ForeignKey('trip.trip_id'), primary_key=True, index=True, nullable=False)
    stop_id = Column(Integer, index=True, nullable=False)
    stop_sequence = Column(Integer, primary_key=True, nullable=False)
    arrival_time = Column(String(9))
    departure_time = Column(String(9), index=True)
    stop_headsign = Column(String(255))
    pickup_type = Column(Integer, default=0)
    drop_off_type = Column(Integer, default=0)
    shape_dist_traveled = Column(Numeric(20, 10))
    timepoint = Column(Integer, default=0)

    id = Column(Integer, primary_key=True, autoincrement=True)
    created = Column(DateTime, default=datetime.datetime.now)
    modified = Column(DateTime, onupdate=datetime.datetime.now)
    deleted = Column(DateTime)


class StopTimeSchema(Schema):
    class Meta:
        ordered = True
        strict = True

    stop_id = fields.Integer()
    stop_code = fields.String()
    stop_name = fields.String()
    stop_desc = fields.String()
    stop_lat = fields.Number()
    stop_lon = fields.Number()
    zone_id = fields.String()
    stop_url = fields.String()
    location_type = fields.Integer()
    parent_station = fields.String()
    stop_timezone = fields.String()
    wheelchair_boarding = fields.Integer()
    platform_code = fields.String()
    direction = fields.String()
    position = fields.String()

    id = fields.Integer(dump_only=True)
    created = fields.DateTime(dump_only=True)
    modified = fields.DateTime(dump_only=True)
    deleted = fields.DateTime(dump_only=True)

    @post_dump
    def create_model(self, data):
        return StopTimeModel(**data)
