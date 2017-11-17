from resources.cloudfront import Cloudfront
from resources.Iteration import IterationResource
from resources.WorkflowRequest  import WorkflowRequestResource

def invoke_resource(resource_name,method_name,params):
    res = RESOURCES[resource_name](**params)
    return getattr(res,ROUTES[method_name])()


RESOURCES = {
    'wf-request': WorkflowRequestResource,
    'iteration': IterationResource,
    'cloudfront': Cloudfront
}

ROUTES = {'GET' : 'get',
          'POST' : 'post',
          'PATCH' : 'patch'
         }
