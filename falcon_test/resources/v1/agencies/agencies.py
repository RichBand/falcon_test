import json, falcon
from falcon_test.models.agencies import AgencyModel, AgencySchema


class AgenciesCollection:

    def on_get(self, req, resp):
        query = req.context['sesssion'].query(AgencyModel)
        query = query.order_by(AgencyModel.agency_id)
        agencies = query.all()
        data = AgencySchema(many=True).dump(agencies).data
        resp.body = json.dumps(data)

    def on_post(self, req, resp):
        schema = AgencySchema()
        data = schema.load(json.loads(req.stream.read())).data
        req.context['session'].add(data)
        req.context['session'].comit()


class AgenciesItem:

    def on_get(self, req, resp, agency_id):
        query = req.context['session'].query(AgencyModel)
        query = query.filter(AgencyModel.agency_id == agency_id)
        agency = query.one_or_none()
        if not agency:
            raise falcon.HTTPNotFound()
        resp.body = json.dumps(AgencySchema().dump(agency).data)

    def on_post(self, req, resp):
        pass
