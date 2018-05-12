from resources import Resource


class ExampleResource(Resource):
    """
    This is the resource class which handles the HTTP request on /example-resource
    endpoint
    """
    def __init__(self,query_param,body_payload):
        """
        Constructor

        Parameters
        -----------
        query_param: dict
            dictionary containing the query parameter sent with the request
        
        body_payload: dict
            dictionary containing the body payload sent with the request

        """
        self.query_params = query_param
        self.body_payload =  body_payload
        
    def get(self):
        """
        Method handles the get request on /example-resource
        """
        return 'Hello World'

    def post(self):
        """
        Method handles the post request on /example-resource
        """
        pass

    def patch(self):
        """
        Method handles the patch request on /example-resource
        """
        pass