import datetime
from marshmallow import Schema, fields, post_load
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, DateTime, Integer, String

BaseModel = declarative_base()


class AgencyModel(BaseModel):
    __tablename__ = 'agency'

    agency_id = Column(Integer, index=True, unique=True)
    agency_name = Column(String(255), nullable=False)
    agency_url = Column(String(255), nullable=False)
    agency_timezone = Column(String(50), nullable=False)
    agency_lang = Column(String(10))
    agency_phone = Column(String(50))
    agency_fare_url = Column(String(255))

    id = Column(Integer, primary_key=True, nullable=True, autoincrement=True)
    created = Column(DateTime, default=datetime.datetime.now)
    modified = Column(DateTime, onupdate=datetime.datetime.now)
    deleted = Column(DateTime)


class AgencySchema(Schema):
    class Meta:
        ordered = True
        strict = True

    agency_id = fields.Integer()
    agency_name = fields.String()
    agency_url = fields.String()
    agency_timezone = fields.String()
    agency_lang = fields.String()
    agency_phone = fields.String()
    agency_fare_url = fields.String()

    id = fields.Integer(dump_only=True)
    created = fields.DateTime(dump_only=True)
    modified = fields.DateTime(dump_only=True)
    deleted = fields.DateTime(dump_only=True)

    @post_load
    def create_model(self, data):
        return AgencyModel(**data)
