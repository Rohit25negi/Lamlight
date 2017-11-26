from distutils.dir_util import copy_tree
import ntpath
import os
import shutil

import boto3

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
    create_package(None)
    zip_path = build_package()
    hlpr.create_lambda_function(name, role, subnet_id, security_group, zip_path)


def create_package(args):
    """
    It create a aws lambda boiler plate for new project to work on. Developer
    can use this boilerplate to put their code on lambda function using lamlight.

    :param args:
    :return:
    """
    destination_path = os.getcwd()
    package_path = os.path.dirname(os.path.realpath(__file__))
    source_path = package_path + os.sep + 'source/'
    copy_tree(source_path, destination_path)
    if not os.path.exists(destination_path + os.sep + 'requirements.txt'):
        open(destination_path + os.sep + 'requirements.txt', 'w').close()


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
        print "code downloaded you can start updating your lambda"
    else:
        print "there is some problem extracting ziped file"


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
    command_list = list()
    os.mkdir("temp_dependencies")

    command_list.append((os.system,("pip install --upgrade pip",)))
    command_list.append((os.system,("pip install  --no-cache-dir -r requirements.txt -t temp_dependencies/",)))
    command_list.append((hlpr.remove_test_cases, ('temp_dependencies/',)))
    hlpr.run_dependent_commands(command_list)

    shutil.make_archive('.requirements', 'zip', 'temp_dependencies/')
    os.rmdir('temp_dependencies/')
    cwd = os.path.basename(os.getcwd())
    shutil.make_archive('/tmp/{}'.format(cwd), 'zip', '.')

    zip_path ="/tmp/{}.zip".format(cwd)
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
    zip_path = build_package()
    hlpr.upload_to_s3(zip_path, bucket_name)
    s3_key = ntpath.basename(zip_path)
    if os.path.exists('.lamlight.conf'):
        hlpr.link_lambda(bucket_name, s3_key)
    print "done pushing"
