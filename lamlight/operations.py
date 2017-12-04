from distutils.dir_util import copy_tree
import ntpath
import os
import shutil
import traceback

import boto3

import constants as consts
import errors
import helper as hlpr
from logger import logger


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
    if hlpr.lambda_function_exists(name):
        raise errors.AWSError(" Lambda function with '{}' name already exists.".format(name))

    logger.info('Creating Scaffolding for lambda function.')
    create_package()
    logger.info('Building Zip.')
    zip_path = build_package()
    logger.info('Creating lambda function.')
    lambda_info = hlpr.create_lambda_function(name, role, subnet_id, security_group, zip_path)
    logger.info('lambda function created. You can start playing with your lambda')
    hlpr.save_lamlight_conf(lambda_info)


def create_package():
    """
    It create a aws lambda boiler plate for new project to work on. Developer
    can use this boilerplate to put their code on lambda function using lamlight.

    """
    destination_path = os.getcwd()
    package_path = os.path.dirname(os.path.realpath(__file__))
    SOURCE = 'source/'
    source_path = package_path + os.sep + SOURCE

    if copy_tree(source_path, destination_path):
        if not os.path.exists(destination_path + os.sep + 'requirements.txt'):
            open(destination_path + os.sep + 'requirements.txt', 'w').close()
    else:
        raise errors.PackagingError(consts.SCAFFOLDING_ERROR)


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
        if not hlpr.lambda_function_exists(lambda_name):
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
        if not hlpr.lambda_function_exists(lambda_name):
            raise errors.AWSError(consts.NO_LAMBDA_FUNCTION.format(lambda_name))    
        logger.info('connecting to aws.')
        client = boto3.client('lambda',region_name=os.getenv('AWS_REGION'))
        lambda_information = client.get_function(FunctionName=lambda_name)
        hlpr.save_lamlight_conf(lambda_information['Configuration'])
        logger.info("Your project is connected to '{}' lambda function".format(lambda_name))
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
    shutil.rmtree('temp_dependencies/')
    os.makedirs("temp_dependencies/")
    
    command_list = list()
    command_list.append((os.system,("pip install --upgrade pip",)))
    command_list.append((os.system,("pip install  --no-cache-dir -r requirements.txt -t temp_dependencies/",)))
    command_list.append((hlpr.remove_test_cases, ('temp_dependencies/',)))
    hlpr.run_dependent_commands(command_list)
    try:
        shutil.make_archive('.requirements', 'zip', 'temp_dependencies/')
        shutil.rmtree('temp_dependencies/')
        cwd = os.path.basename(os.getcwd())
        zip_path = "/tmp/{}".format(cwd)
        shutil.make_archive(zip_path, 'zip', '.')
        zip_path+='.zip'
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
    account_id = boto3.client('sts',region_name=os.getenv('AWS_REGION')).get_caller_identity().get('Account')

    bucket_name = 'lambda-code-{}'.format(account_id)
    hlpr.create_bucket(bucket_name)

    logger.info('building zip')
    zip_path = build_package()
    logger.info("uploading code base to S3")
    hlpr.upload_to_s3(zip_path, bucket_name)

    s3_key = ntpath.basename(zip_path)
    hlpr.link_lambda(bucket_name, s3_key)
    logger.info("Lambda updation complete")



