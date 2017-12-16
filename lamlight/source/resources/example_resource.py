from resources import Resource


class ExampleResource(Resource):

    def __init__(self,query_param,body_payload):
        
        self.query_params = query_param
        self.body_payload =  body_payload
        
    def get(self):
        return 'Hello World'

    def post(self):
        pass

    def patch(self):
        pass