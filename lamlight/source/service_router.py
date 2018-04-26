'''
 This module is the responsible invoking the appropriate resource methods depending
 on the request to the microservice provider(lambda for now).
 having this module prevent any change in the rest of the code base. Rest of the code
 base will be indipendent of the deployment.

'''
import json
import sys

import unzip_requirements


import constants as res_const
from resources import helper
from  resources.resource_list import RESOURCES,ROUTES
from resources.resource_list import invoke_resource


def respond(err, res=None):
    '''
    To prepare the response payload with the  headers required for the
    cross origin access of the lambda functions through the api gateway.
    
    PARAMETERS
    -------------
    err : Exception
        errors
    res : Dict
        response to be sent
    '''
    return {
        'statusCode': '400' if err else '200',
        'body': err.message if err else json.dumps(res),
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin':'*'
        },
    }
    
def main(event, context):
    '''
        This is the main handler function which is executed first when the lambda function
        is invoked.
        This functions is invoked by aws lambda by passing the following arguments:
        1) event
        2) context
        For more information refer :
        http://docs.aws.amazon.com/lambda/latest/dg/python-programming-model-handler-types.html

        This functions inturn call all the working functions and returns the result fetched
        from these functions.
    
    PARAMETERS
    ------------
    event : dict
        Object that contains all the parameters passed while invoking the lambda function
    context : LambdaContext
        object that contains the runtime information about the lambda function.
 
    RETURNS
    ------------
    response : dict
        response to the caller
    '''

    resource_name = resource(event)
    method_name = http_method(event)
    params = parameters(event)
    result = invoke_resource(resource_name,method_name,params)
    return respond(None,result)

def resource(event):
    '''
    This function returns the resource name on which the client requested.

    PARAMETERS
    ----------
    event : dict
        Object that contains all the parameters passed while invoking
        the lambda function
    
    RETURNS
    -------
    str:
        Name of the resource

    '''
    RESOURCE = 'resource'
    return event[RESOURCE][1:]

def http_method(event):
    '''
    This function returns the HTTP Method name with which the client requested
    the resource.

    PARAMETERS
    ----------
    event : dict
        Object that contains all the parameters passed while invoking
        the lambda function
    
    RETURNS
    -------
    str:
        Name of the HTTP Method

    '''
    HTTP_METHOD = "httpMethod"

    return event[HTTP_METHOD]

def parameters(event):
    '''
    This function returns the data that has been sent with request from
    the client.

    PARAMETERS
    ----------
    event : dict
        Object that contains all the parameters passed while invoking
        the lambda function
    
    RETURNS
    -------
    Dict:
        Dict that contains the query_params and the body data. Example value
        could be :
            {
                'query_param':{'id':1999}
                'body_payload':{'state':'state','value':'completed'}
            }

    '''
    QUERY_PARAM_STRING = 'queryStringParameters'
    BODY = 'body'
    return {res_const.RESOURCE_QUERY_DATA : event[QUERY_PARAM_STRING],
            res_const.RESOURCE_PAYLOAD_DATA : json.loads(event[BODY]) if (event[BODY]) else None }

if __name__=='__main__':
    '''
        This call to main function is to test the package from the console.
        while running the main module from the console resource name and method
        is to be entered as first CL agrument.
    '''
    event_data = {'body':json.dumps({"id":859}),'resource':sys.argv[1],'httpMethod':sys.argv[2],
            'queryStringParameters':{"id":859}
                 }
    main(event_data,None)