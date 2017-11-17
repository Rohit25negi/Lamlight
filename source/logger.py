
WORKFLOW_REQUEST_ID = None
def log_to_cloudwatch(log_marker, message):
    '''
    This functions is used to print the log messages so that they can be logged
    to cloudwatch.

    PARAMETERS
    ----------
    message : str
        message to be logged

    '''
    wf_message = ':: For workflow request '+str(WORKFLOW_REQUEST_ID)+' ::'
    print log_marker + wf_message
    print message
