from distutils.dir_util import copy_tree
import ntpath
import os
import shutil

import boto3

import constants as consts
import helper as hlpr


def create_lambda(name, role, subnet_id, security_group):
    """
    This function creates the lambda is used to create a new aws lambda
    project.

    :param name:
    :param role:
    :param subnet_id:
    :param security_group:
    :return:
    """
    print 'Creating project structure'
    create_package()
    print 'Project structure created'
    print 'Building code zip'
    zip_path = build_package()
    print 'creating lambda function'
    hlpr.create_lambda_function(name, role, subnet_id, security_group, zip_path)
    print 'lambda function created. You can start playing with your lambda'

def create_package():
    """
    It create a aws lambda boiler plate for new project to work on. Developer
    can use this boilerplate to put their code on lambda function using lamlight.

    :param:
    :return:
    """
    destination_path = os.getcwd()
    package_path = os.path.dirname(os.path.realpath(__file__))
    SOURCE = 'source/'
    source_path = package_path + os.sep + SOURCE
    if copy_tree(source_path, destination_path):
        if not os.path.exists(destination_path + os.sep + 'requirements.txt'):
            open(destination_path + os.sep + 'requirements.txt', 'w').close()
    else:
        print "project cannot be created"


def update_lamda(lambda_name):
    """
    This function downloads the code running on a given lambda function.
    This code is downloaded in CWD.

    :param lambda_name:
            Name of the lambda function
    :return:
    """
    client = boto3.client('lambda')
    lambda_information = client.get_function(FunctionName=lambda_name)

    code_location = lambda_information['Code']['Location']
    download_file_path = hlpr.download_object(code_location)
    if hlpr.extract_zipped_code(download_file_path):
        hlpr.save_lamlight_conf(lambda_information['Configuration'])
        return True
    else:
        print False


def test_package(args):
    """

    :param args:
    :return:
    """
    #TODO to allow developer to test his/her lambda function locally
    pass


def build_package():
    """
    This functions builds the code package to put on aws lambda function.
    Zip package prepared by this function is stored in /tmp/<project-name>.zip
    location.

    :return zip_path:
            path of the zip package

    """
    os.mkdir("temp_dependencies")

    command_list = list()
    command_list.append((os.system,("pip install --upgrade pip",)))
    command_list.append((os.system,("pip install  --no-cache-dir -r requirements.txt -t temp_dependencies/",)))
    command_list.append((hlpr.remove_test_cases, ('temp_dependencies/',)))
    hlpr.run_dependent_commands(command_list)

    shutil.make_archive('.requirements', 'zip', 'temp_dependencies/')
    os.rmdir('temp_dependencies/')
    cwd = os.path.basename(os.getcwd())
    zip_path = "/tmp/{}.zip".format(cwd)
    shutil.make_archive(zip_path, 'zip', '.')

    return zip_path


def push_code():
    """
    This functions pushes the current state of the working project
    to lambda function.
    :return:
    """
    account_id = boto3.client('sts').get_caller_identity().get('Account')
    bucket_name = 'lambda-code-{}'.format(account_id)
    hlpr.create_bucket(bucket_name)
    print "Building code zip"
    zip_path = build_package()
    print "Done building code base"
    print "uploading code base to S3"
    hlpr.upload_to_s3(zip_path, bucket_name)
    print "Code is uploaded"
    s3_key = ntpath.basename(zip_path)
    if os.path.exists(consts.LAMLIGHT_CONF):
        hlpr.link_lambda(bucket_name, s3_key)
        return True
    else:
        print "Current project is not a lamlight project"
        return False


