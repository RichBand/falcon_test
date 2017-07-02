from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

BaseModel = declarative_base()


class DatabaseComponent:
    def __init__(self):
        self.engine = create_engine('sqlite:///PeterboroughTransit.db')
        self.Session = sessionmaker(bind=self.engine)
        BaseModel.metadata.create_all(bind=self.engine)

    def process_request(self, req, resp):
        req.context['session'] = self.Session()

    def process_response(self, req, resp, resource, req_succeeded):
        req.context['session'].close()
