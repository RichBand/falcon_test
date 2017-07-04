from wsgiref.simple_server import make_server
from falcon_test.server import Application


if __name__ == '__main__':
    httpd = make_server('', 80, Application())
    httpd.handle_request()
    httpd.serve_forever(poll_interval=0.5)
