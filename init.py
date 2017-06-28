# things.py

# Let's get this party started!
import falcon, json, sqlite3

from wsgiref.simple_server import make_server


# Falcon follows the REST architectural style, meaning (among
# other things) that you think in terms of resources and state
# transitions, which map to HTTP verbs.

class CharacterCollection(object):

    def on_get(self, req, resp):
        """Handles GET requests"""
        _field_names = ('name', 'sex', 'hair', 'alive')
        param_fields = list(req.params.keys())

        if not set(param_fields).issubset(_field_names):
            raise falcon.HTTPBadRequest(
                'Bad Request',
                'invalid parameters: ' + ', '.join(set(param_fields) - set(_field_names))
            )
        elif req.params:
            characters = req.cur.execute(
                'SELECT * FROM characters where ' + self.get_params(param_fields),
                req.params).fetchall()
        elif not req.params:
            characters = req.cur.execute('SELECT * FROM characters;').fetchall()

        resp.body = json.dumps(characters)

    def on_post(self, req, resp):
        data = json.loads(req.stream.read())
        errors = self.validate_character(data)

        if errors:
            raise falcon.HTTPBadRequest('Bad Request', ''.join(errors))
        else:
            try:
                req.cur.execute(
                    'INSERT INTO characters (id, name, sex, hair, alive) values (?, ?, ?, ?, ?)',
                    (None, data['name'], data['sex'], data['hair'], data['alive']))
            except ValueError:
                raise falcon.HTTPError(falcon.HTTP_202, 'Error', )
        req.conn.commit()
        resp.status = falcon.HTTP_202

    @staticmethod
    def validate_character(data):
        _hair = ('yellow', 'blue', 'brown', 'black', 'white', 'bald')
        _sex = ('male', 'female', 'undefined')
        errors = []
        errors.append('name can\'t be empty') if not len(data['name']) else None
        errors.append('wrong hair type') if 'hair' not in data or data['hair'] not in _hair else None
        errors.append('wrong sex type') if 'sex' not in data or data['sex'] not in _sex else None
        return errors

    @staticmethod
    def get_params(params: list):
        return 'and '.join('{0}=:{0} '.format(param) for param in params)


class ContentComponent:

    def __init__(self, content_type):
        self.content_type = content_type

    def process_response(self, req, resp, resource, req_succeeded):
        resp.content_type = 'application/json'


class DatabaseComponent:

    def __init__(self):
        self.conn = sqlite3.connect("Simpsons.db")
        cursor = self.conn.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS characters (id INTEGER PRIMARY KEY, name VARCHAR(20), sex VARCHAR(20), hair VARCHAR(20), alive BOOLEAN )' )
        self.conn.commit()

        cursor.close()

    def process_request(self, req, resp):
        req.cur = self.conn.cursor()
        req.conn = self.conn

    def process_response(self, req, resp, resource, req_succeeded):
        pass
        # req.conn.close()


class Application(falcon.API):

    def __init__(self):
        self.database_component = DatabaseComponent()  # DB is create here
        self.content_type_component = ContentComponent(content_type='application/json')
        super().__init__(middleware=[self.database_component, self.content_type_component])
        self.add_route('/characters', CharacterCollection())


httpd = make_server('', 80, Application())
httpd.handle_request()
httpd.serve_forever(poll_interval=0.5)
