import datetime
from marshmallow import Schema, fields, post_dump
from sqlalchemy.orm import relationship
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
    __tablename__ = 'stop'

    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(50))
    name = Column(String(255), nullable=False)
    desc = Column(String(255))
    lat = Column(Numeric(12, 9), nullable=False)
    lon = Column(Numeric(12, 9), nullable=False)
    zone_id = Column(String(50))
    url = Column(String(255))
    location_type = Column(Integer, index=True, default=0)
    parent_station = Column(String(255))
    timezone = Column(String(50))
    wheelchair_boarding = Column(Integer, default=0)
    platform_code = Column(String(50))
    direction = Column(String(50))
    position = Column(String(50))

    created = Column(DateTime, default=datetime.datetime.now)
    modified = Column(DateTime, onupdate=datetime.datetime.now)
    deleted = Column(DateTime)

    stop_times = relationship(
        'stop_time',
        primaryjoin='stop.id==stop_time.stop_id',
        foreign_keys='(stop.id)',
        uselist=True, viewonly=True)


class StopSchema(Schema):
    class Meta:
        ordered = True
        strict = True

    id = fields.Integer()
    code = fields.String()
    name = fields.String()
    desc = fields.String()
    lat = fields.Number()
    lon = fields.Number()
    zone_id = fields.String()
    url = fields.String()
    location_type = fields.Integer()
    parent_station = fields.String()
    timezone = fields.String()
    wheelchair_boarding = fields.Integer()
    platform_code = fields.String()
    direction = fields.String()
    position = fields.String()

    created = fields.DateTime(dump_only=True)
    modified = fields.DateTime(dump_only=True)
    deleted = fields.DateTime(dump_only=True)

    @post_dump
    def create_model(self, data):
        return StopModel(**data)
