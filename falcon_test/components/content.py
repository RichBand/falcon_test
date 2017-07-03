class ContentComponent:
    def __init__(self, content_type):
        self.content_type = content_type

    def process_response(self, req, resp, resource, req_succeeded):
        resp.content_type = 'application/json'
