"""
This Module contains the utilities related to the aws lambda functions.
Module contains the  following functions:
    1) create_lambda_function : To create a lambda function.
    2) link_lambda: To link the zip present in s3 to lambda function.
    3) lambda_function_exists: To check the existance of the lambda function with name.
"""
import configparser
import os

import boto3

from lamlight import constants as consts
from lamlight import errors, helper
from lamlight.aws_resources import ec2_utils


def default_lambda_details():
    """
    Returns the default lambda details.

    Returns
    --------
    lambda_function_details: dict
        default lambda function details for python2.7
    """

    lambda_function_details = dict()
    lambda_function_details['Runtime'] = 'python2.7'
    lambda_function_details['Handler'] = 'service_router.main'

    return lambda_function_details


def create_lambda_function(name, role, subnet_id, security_group, zip_path):
    """
    This function creates the lambda function with the given information
    passed as the arguments.

    Parameters
    -----------
    name: str
            Name of the lambda function
    role: str
            IAM Role to be assigned to the lambda function
    subnet_id: str
            Subnet to be assgined to the lambda function
    security_group: str
            Security group to be assigned to the lambda function
    zip_path: str
            zip path which contains the code to be uploaded on lambda function
    :return:
    """
    try:
        lambda_details = default_lambda_details()
        #Role is must
        if not role:
            lambda_details['Role'] = role
            #role = ec2_utils.get_role()

        if subnet_id and security_group:
            lambda_details['VpcConfig'] = {'SubnetIds': [subnet_id], 
                                           'SecurityGroupIds': [security_group]}
            #subnet_id = ec2_utils.get_subnet_id()
            #security_group = ec2_utils.get_security_group()

        client = boto3.client('lambda', region_name=os.getenv('AWS_REGION'))
        lambda_details['FunctionName'] = name
        
        lambda_details['Code'] = {'ZipFile': open(zip_path).read()}
        lambda_info = client.create_function(**lambda_details)

        return lambda_info
    except Exception as error:
        raise errors.AWSError(error.message)


def link_lambda(bucket_name, s3_key):
    """
    It links the code package on s3 bucket to the lambda function.

    Parameters
    -----------
    bucket_name: str
           Name of the bucket where the code package is present
    s3_key: str
           Key of the code package

    """
    client = boto3.client('lambda', region_name=os.getenv('AWS_REGION'))
    parser = helper.read_configuration_file()
    client.update_function_code(FunctionName=parser['LAMBDA_FUNCTION']['funtionname'],
                                S3Bucket=bucket_name, S3Key=s3_key)


def lambda_function_exists(name):
    """
    It checks whether the lambda function with the given name exists or not.

    Parameters
    -----------
    name : str:
        name of the lambda function

    Returns
    --------
    bool:
        True if the lambda function with the given name exists. Else, False
    """
    try:
        client = boto3.client('lambda', region_name=os.getenv('AWS_REGION'))
        client.get_function(FunctionName=name)
        return True
    except Exception:
        return False
