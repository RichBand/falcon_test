# things.py

# Let's get this party started!
import falcon, json, sqlite3

from wsgiref.simple_server import make_server


# Falcon follows the REST architectural style, meaning (among
# other things) that you think in terms of resources and state
# transitions, which map to HTTP verbs.

class CharacterCollection(object):

    @staticmethod
    def on_get(req, resp):
        """Handles GET requests"""
        characters = req.conn.execute('SELECT * FROM characters;').fetchall()
        resp.body = json.dumps(characters)

    @staticmethod
    def on_post(self, req, resp):
        data = json.loads(req.stream.read())
        errors = self.validate_character(data)

        if errors:
            raise falcon.HTTPBadRequest('Bad Request', ''.join(errors))
        else:
            try:
                req.conn.execute(
                    'INSERT INTO characters (id, name, gender, hair, alive) values (?, ?, ?, ?, ?)',
                    (None, data['name'], data['gender'], data['hair'], data['alive']))

            except ValueError:
                raise falcon.HTTPError(falcon.HTTP_202, 'Error', )

        resp.status = falcon.HTTP_202

    @staticmethod
    def validate_character(self, data):
        _hair = ('yellow', 'blue', 'brown', 'black', 'white', 'bald')
        _gender = ('male', 'female', 'undefined')
        errors = []
        errors.append('name can\'t be empty') if data['name'] not in _hair else None
        errors.append('wrong hair type') if data['hair'] not in _hair else None
        errors.append('wrong gender type') if data['gender'] not in _gender else None
        return errors


class ContentComponent:

    def __init__(self, content_type):
        self.content_type = content_type

    def process_response(self, req, resp, resource, req_succeeded):
        resp.content_type = 'application/json'


class DatabaseComponent:

    def __init__(self):
        self.conn = sqlite3.connect("Simpsons.db")
        cursor = self.conn.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS characters (id INTEGER PRIMARY KEY, name VARCHAR(20), gender VARCHAR(20), hair VARCHAR(20), alive BOOLEAN )' )
        self.conn.commit()
        cursor.close()

    def process_request(self, req, resp):
        req.conn = self.conn.cursor()

    def process_response(self, req, resp, resource, req_succeeded):
        req.conn.close()


class Application(falcon.API):

    def __init__(self):
        self.database_component = DatabaseComponent()  # DB is create here
        self.content_type_component = ContentComponent(content_type='application/json')
        super().__init__(middleware=[self.database_component, self.content_type_component])
        self.add_route('/characters', CharacterCollection())


httpd = make_server('', 80, Application())
httpd.handle_request()
httpd.serve_forever(poll_interval=0.5)
