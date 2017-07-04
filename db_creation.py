from sqlalchemy import create_engine
from falcon_test.models.base import BaseModel
from falcon_test.models.agencies import AgencyModel
from falcon_test.models.calendars import CalendarModel
from falcon_test.models.routes import RouteModel
from falcon_test.models.stops import StopModel
from falcon_test.models.stops_time import StopTimeModel
from falcon_test.models.trips import TripModel


def database_creator():
    engine = create_engine('sqlite:///PeterboroughTransit.db')
    BaseModel.metadata.create_all(bind=engine)

if __name__ == '__main__':
    database_creator()
