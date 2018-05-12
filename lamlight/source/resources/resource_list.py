from resources.example_resource import ExampleResource


def invoke_resource(resource_name, method_name, params):
    """
    Function invokes the relevent method of relavent class
    depending on the request.

    Parameters
    -----------
    resource_name: str
        Name of the resource on which the request came
    
    method_name : str
        Http method name with which request is made
    
    params: dict
        Parameters passed with thes request
    
    Returns
    --------
    dict:
        Response
    """
    res = RESOURCES[resource_name](**params)
    return getattr(res, ROUTES[method_name])()


RESOURCES = {
    'example-resource': ExampleResource,

}

ROUTES = {'GET': 'get',
          'POST': 'post',
          'PATCH': 'patch'
          }
