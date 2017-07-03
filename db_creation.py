from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from falcon_test.models import agencies, calendars, routes, stops, trips

BaseModel = declarative_base()


class DatabaseCreator:
    def __init__(self):

        engine = create_engine('sqlite:///PeterboroughTransit.db')
        session = sessionmaker(bind=engine)

        agency = agencies.AgencyModel()
        calendar = calendars.CalendarModel()
        route = routes.RouteModel()
        stop = stops.StopModel()
        trip = trips.TripModel()
        BaseModel.metadata.create_all(bind=engine)

DatabaseCreator()
