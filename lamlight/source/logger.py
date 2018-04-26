'''
Module defines a logger to send the logs to cloud watch from lambda function
'''


def log_to_cloudwatch(log_marker, message):
    '''
    This functions is used to print the log messages so that they can be logged
    to cloudwatch.

    PARAMETERS
    ----------
    message : str
        message to be logged

    '''
    print log_marker,
    print ' : ',
    print message
