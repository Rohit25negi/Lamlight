"""
Module defines the functions for various  lamlight operations.

This modules contains the functions for the following lamlight operations:
    1) creating new lamlight project
    2) updating existing lambda code
    3) connecting existing lambda function
    4) pushing the changed code directly to lambda function

"""
import ntpath
import os
import shutil

import boto3

from lamlight.aws_resources import lambda_utils
from lamlight.aws_resources import s3_utils

from lamlight import constants as consts
from lamlight import errors
from lamlight import helper as hlpr
from lamlight.logger import logger


def create_lambda(name, role, subnet_id, security_group):
    """
    This function creates the lambda is used to create a new aws lambda
    project.

    Parameters:
    ------------
    name: str
        name of the lambda function
    role: str
        IAM role ARN to be assigned to lambda function
    subnet_id: str
        subnet id to be assigned to lambda function
    security_group: str
        security group id to be assigned to lambda function
    
    """
    if lambda_utils.lambda_function_exists(name):
        raise errors.AWSError(" Lambda function with '{}' name already exists.".format(name))

    logger.info('Creating Scaffolding for lambda function.')
    hlpr.create_package()
    logger.info('Building Zip.')
    zip_path = build_package()
    logger.info('Creating lambda function.')
    lambda_info = lambda_utils.create_lambda_function(name, role, subnet_id, security_group, zip_path)
    logger.info('lambda function created. You can start playing with your lambda')
    hlpr.save_lamlight_conf(lambda_info)


def update_lamda(lambda_name):
    """
    This function downloads the code running on a given lambda function.
    This code is downloaded in CWD.

    Parameters
    -----------
    lambda_name :str
        Lambda function name
    """
    try:
        if not lambda_utils.lambda_function_exists(lambda_name):
            raise errors.AWSError(consts.NO_LAMBDA_FUNCTION.format(lambda_name))

        logger.info('connecting to aws.')
        client = boto3.client('lambda',region_name=os.getenv('AWS_REGION'))
        lambda_information = client.get_function(FunctionName=lambda_name)

        logger.info('downloading code base.')
        code_location = lambda_information['Code']['Location']
        download_file_path = hlpr.download_object(code_location)
        logger.info('Extracting code.')
    except Exception as error:
        raise errors.AWSError(error.message)
    try:
        hlpr.extract_zipped_code(download_file_path)
        hlpr.save_lamlight_conf(lambda_information['Configuration'])
    except Exception as error:
        raise errors.PackagingError(consts.CODE_PULLING_ERROR.format(lambda_name))


def connect_lambda(lambda_name):
    """
    It get the information of a lambda function and save the configuration
    file in the current project.

    Parameters
    -----------
    lambda_name: str
        name of the lambda function
    """
    try:
        if not lambda_utils.lambda_function_exists(lambda_name):
            raise errors.AWSError(consts.NO_LAMBDA_FUNCTION.format(lambda_name))
        logger.info('connecting to aws.')
        client = boto3.client('lambda', region_name=os.getenv('AWS_REGION'))
        lambda_information = client.get_function(FunctionName=lambda_name)
        hlpr.save_lamlight_conf(lambda_information['Configuration'])
        logger.info("Your project is connected to '%s' lambda function" %(lambda_name))
    except Exception as error:
        raise errors.PackagingError(error.message)


def build_package():
    """
    This functions builds the code package to put on aws lambda function.
    Zip package prepared by this function is stored in /tmp/<project-name>.zip
    location.

    Returns
    --------
    zip_path: str
        path of the zip package

    """
    if os.path.exists('temp_dependencies/'):
        shutil.rmtree('temp_dependencies/')

    if os.path.exists('.requirements.zip'):
        os.remove('.requirements.zip')

    os.makedirs("temp_dependencies/")

    command_list = list()
    command_list.append((os.system, ("pip install --upgrade pip",)))
    command_list.append((os.system, ("pip install  --no-cache-dir -r requirements.txt -t temp_dependencies/",)))
    command_list.append((hlpr.remove_trees, ('temp_dependencies/',)))
    hlpr.run_dependent_commands(command_list)
    try:
        os.system('cd temp_dependencies && zip -r ../.requirements.zip -i .')
        shutil.rmtree('temp_dependencies/')
        cwd = os.path.basename(os.getcwd())
        zip_path = "/tmp/{}".format(cwd)
        shutil.make_archive(zip_path, 'zip', '.')
        zip_path += '.zip'
    except Exception:
        raise errors.PackagingError(consts.PACKAGIN_ERROR)
    return zip_path


def push_code():
    """
    This functions pushes the current state of the working project
    to lambda function.

    """
    if not os.path.exists(consts.LAMLIGHT_CONF):
        raise errors.NoLamlightProject(consts.NO_LAMLIGHT_PROJECT)

    logger.info('Getting aws user identity')
    sts = boto3.client('sts', region_name=os.getenv('AWS_REGION'))
    account_id = sts.get_caller_identity().get('Account')
    my_session = boto3.session.Session()
    my_region = my_session.region_name

    if not my_region:
        my_region = os.getenv('AWS_REGION')

    bucket_name = 'lambda-code-{}-{}'.format(account_id,my_region)
    s3_utils.create_bucket(bucket_name)

    logger.info('building zip')
    zip_path = build_package()
    logger.info("uploading code base to S3")
    s3_utils.upload_to_s3(zip_path, bucket_name)

    s3_key = ntpath.basename(zip_path)
    lambda_utils.link_lambda(bucket_name, s3_key)
    logger.info("Lambda updation complete")
