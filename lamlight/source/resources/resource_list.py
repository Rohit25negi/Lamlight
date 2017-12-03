from resources.example_resource import ExampleResource

def invoke_resource(resource_name,method_name,params):
    res = RESOURCES[resource_name](**params)
    return getattr(res,ROUTES[method_name])()


RESOURCES = {
    'example-resource': ExampleResource,

}

ROUTES = {'GET' : 'get',
          'POST' : 'post',
          'PATCH' : 'patch'
         }
