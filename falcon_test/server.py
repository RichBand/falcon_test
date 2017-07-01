import falcon
# TODO: why did I need to add "falcon_test" and not just the dot is because the setup.py is not 'setup'?
from falcon_test.components import DatabaseComponent, ContentComponent
from falcon_test.resources import v1


class Application(falcon.API):
    def __init__(self):
        self.database_component = DatabaseComponent()
        self.content_type_component = ContentComponent(content_type='application/json')
        super().__init__(middleware=[self.database_component, self.content_type_component])

        self.add_route('/v1/routes', v1.routes.RoutesCollection())
        self.add_route('/v1/routes/{route_id}', v1.routes.RoutesItem())
