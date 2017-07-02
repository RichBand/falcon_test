import json, falcon
from falcon_test.models.routes import RouteModel, RouteSchema


class RoutesCollection:

    def on_get(self, req, resp):
        query = req.context['session'].query(RouteModel)
        query = query.order_by(RouteModel.route_id)
        routes = query.all()
        data = RouteSchema(many=True).dump(routes).data
        resp.body = json.dumps(data)

    #TODO: what's semantically correct to post a route? feel like this should be in Items, but then I need to send a route_id to post?
    def on_post(self, req, resp):
        route_schema = RouteSchema()
        data = route_schema.load(json.loads(req.stream.read())).data
        req.context['session'].add(data)
        req.context['session'].commit()

    def on_put(self, req, resp):
        route_schema = RouteSchema()
        data = route_schema.load(json.loads(req.stream.read())).data
        query = req.context['session'].query(RouteModel)
        route = query.filter(RouteModel.route_id == data.route_id).one_or_none()
        # #TODO: how to do this: route.update(data)?
        # for key in data.keys():
        #     route[key] == data[key]
        req.context['session'].commit()


class RoutesItem:

    def on_get(self, req, resp, route_id):
        query = req.context['session'].query(RouteModel)
        query = query.filter(RouteModel.route_id == route_id)
        route = query.one_or_none()
        if not route:
            raise falcon.HTTPNotFound()
        resp.body = json.dumps(RouteSchema().dump(route).data)

    def on_delete(self, req, route_id):
        query = req.context['session'].query(RouteModel)
        query = query.filter(RouteModel.route_id == route_id)
        route = query.one_or_none()
        if not route:
            raise falcon.HTTPNotFound()
        req.context['session'].delete(route)
        req.context['session'].commit()
