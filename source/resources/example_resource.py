from resources import Resource

class ExampleResource(Resource):


    def get(self):
        return 'hello'

    def post(self):
        pass

    def patch(self):
        pass