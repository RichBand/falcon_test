import datetime
from marshmallow import Schema, fields, post_load
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, DateTime, Integer, String

BaseModel = declarative_base()


class AgencyModel(BaseModel):
    __tablename__ = 'agency'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String(255), nullable=False)
    url = Column(String(255), nullable=False)
    timezone = Column(String(50), nullable=False)
    lang = Column(String(10))
    phone = Column(String(50))
    fare_url = Column(String(255))

    created = Column(DateTime, default=datetime.datetime.now)
    modified = Column(DateTime, onupdate=datetime.datetime.now)
    deleted = Column(DateTime)


class AgencySchema(Schema):
    class Meta:
        ordered = True
        strict = True

    id = fields.Integer()
    name = fields.String()
    url = fields.String()
    timezone = fields.String()
    lang = fields.String()
    phone = fields.String()
    fare_url = fields.String()

    created = fields.DateTime(dump_only=True)
    modified = fields.DateTime(dump_only=True)
    deleted = fields.DateTime(dump_only=True)

    @post_load
    def create_model(self, data):
        return AgencyModel(**data)
