import json, falcon
from falcon_test.models.calendars import CalendarModel, CalendarSchema


class CalendarsCollection:

    def on_get(self, req, resp):
        query = req.context['session'].query(CalendarModel)
        query = query.order_by(CalendarModel.id)
        services = query.all()
        data = CalendarSchema(many=True).dump(services).data
        resp.body = json.dumps(data)

    def on_post(self, req, resp):
        data = CalendarSchema().load(json.loads(req.stream.read())).data
        req.context['session'].add(data)
        req.context['session'].commit()


class CalendarItem:

    def on_get(self, req, resp):
        pass

    def on_post(self, req, resp):
        pass
