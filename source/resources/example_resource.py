from resources import Resource


class ExampleResource(Resource):

    def get(self):
        return 'Hello World'

    def post(self):
        pass

    def patch(self):
        pass