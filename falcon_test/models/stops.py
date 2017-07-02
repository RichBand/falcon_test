import datetime
from marshmallow import Schema, fields, post_dump
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, DateTime, Integer, Numeric,  String

BaseModel = declarative_base()


class StopModel(BaseModel):
    """
    wheelchair_boarding:
    0 (or empty): Indicates that there is no accessibility information for the stop
    1: Indicates that at least some vehicles at this stop can be boarded by a rider in a wheelchair
    2: Wheelchair boarding is not possible at this stop
    """
    __tablename__ = 'stops'

    stop_id = Column(Integer, primary_key=True, index=True, nullable=False)
    stop_code = Column(String(50))
    stop_name = Column(String(255), nullable=False)
    stop_desc = Column(String(255))
    stop_lat = Column(Numeric(12, 9), nullable=False)
    stop_lon = Column(Numeric(12, 9), nullable=False)
    zone_id = Column(String(50))
    stop_url = Column(String(255))
    location_type = Column(Integer, index=True, default=0)
    parent_station = Column(String(255))
    stop_timezone = Column(String(50))
    wheelchair_boarding = Column(Integer, default=0)
    platform_code = Column(String(50))
    direction = Column(String(50))
    position = Column(String(50))

    id = Column(Integer, primary_key=True, autoincrement=True)
    created = Column(DateTime, default=datetime.datetime.now)
    modified = Column(DateTime, onupdate=datetime.datetime.now)
    deleted = Column(DateTime)


class StopSchema(Schema):
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
        return StopModel(**data)
