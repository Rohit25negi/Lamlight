import json
import ntpath
import os
import shutil
import tempfile
import urllib
import zipfile

import boto3


def run_dependent_commands(command_list):
    """
    This fucntions executes a list of dependent commands. In which,
    each command is dependent on the success of its previous command.
    If one command fails, remaining commands are not executed.

    :param command_list:
        list of commands and their arguments
    :return:
    """
    for command in command_list:
        assert not command[0](*command[1])
    

def remove_test_cases(path):
    """
    This functions is used to remove the test cases from the heavy
    pip packages.
    :param path:
           path from which the test cases are to be removed
    :return:
    """
    for root, dirs, files in os.walk(path):
        print root
        print dirs

        for dir in dirs:
            path=root+os.sep+dir
            
            if os.path.isdir(path) and 'tests' in dir: 
                try:
                    print "to delete"
                    shutil.rmtree(path)
                except Exception as err:
                    print err.message
                    return 1
    return 0

            
def download_object(url):
    """
    This function is used to download the code package from
    a given url.

    :param url:
           url from which file is to be downloaded

    :return download_file_path:
            path where the code package is downloaded
    """
    temp_dir_path = tempfile.mkdtemp(dir='/tmp')
    download_file_path = temp_dir_path+os.sep+"pet.zip"
    urllib.urlretrieve(url,download_file_path)
    return download_file_path


def extract_zipped_code(zipped_code):
    """
    This function extracts the zip file in the CWD.
    :param zipped_code:
           path to zip file which is to be extracted
    :return:
    """
    with zipfile.ZipFile(zipped_code,'r') as zip_ref:
        zip_ref.extractall()
    return True

def save_lamlight_conf(lambda_information):
    """
    This functions saves the lambda configuration file to the CWD.
    Lambda cofiguration file contains the information of the lambda
    function to which current project is associated to.

    :param lambda_information:
    :return:
    """
    conf_file = '.lamlight.conf'
    f = open(conf_file,'w')
    json.dump(lambda_information,f)

def create_bucket(bucket_name):
    """
    This function creates a new bucket with name 'bucket_name' is
    already not exists.

    :param bucket_name:
           Name of bucket to be created
    :return:

    """
    res = boto3.resource("s3")
    if res.Bucket(bucket_name) not in res.buckets.all():
        s3 = boto3.client("s3")
        s3.create_bucket(Bucket=bucket_name,CreateBucketConfiguration={
        'LocationConstraint': 'ap-southeast-1'})


def upload_to_s3(zip_path,bucket_name):
    """
    This function uploads a file to the bucket with name 'bucket_name'

    :param zip_path:
           zip file to be uploaded to bucket
    :param bucket_name:
           Name of the bucket to which the file is to be uploaded
    :return file_url:
           s3 url of the uploaded file.

    """
    s3 = boto3.client('s3')
    zip_path = os.path.expanduser(zip_path)
    file_name = ntpath.basename(zip_path)
    print file_name
    s3.upload_file(zip_path,bucket_name,file_name)
    file_url = '%s/%s/%s' % (s3.meta.endpoint_url, bucket_name, file_name)
    return file_url

def link_lambda(bucket_name, s3_key):
    """

    :param bucket_name:
    :param s3_key:
    :return:
    """
    client = boto3.client('lambda')
    lamlight_conf = json.load(open('.lamlight.conf'))
    print json.dumps(lamlight_conf,indent=2)
    client.update_function_code(FunctionName=lamlight_conf['FunctionName'],
                                S3Bucket=bucket_name, S3Key=s3_key)

def create_lambda_function(name, role, subnet_id, security_group,zip_path):
    """

    :param name:
    :param role:
    :param subnet_id:
    :param security_group:
    :param zip_path:
    :return:
    """
    if not role:
        role = get_role()
    if not subnet_id:
        subnet_id = get_subnet_id()

    if not security_group:
        security_group = get_security_group()

    client = boto3.client('lambda')
    lambda_details = default_lambda_details()
    lambda_details['FunctionName'] = name
    lambda_details['Role'] = role
    lambda_details['VpcConfig'] = {'SubnetIds':[subnet_id],'SecurityGroupIds':[security_group]}
    lambda_details['Code'] = {'ZipFile':open(zip_path).read()}

    lambda_info = client.create_function(**lambda_details)
    save_lamlight_conf(lambda_info)


def get_subnet_id():
    """

    :return:
    """
    client = boto3.client('ec2')
    subnets = client.describe_subnets()
    print json.dumps(subnets,indent=2,default=str)
    subnet_id = raw_input('enter the subnet id you want to allocate to your lambda function')
    return subnet_id

def default_lambda_details():
    """

    :return:
    """
    lambda_function_details = dict()
    lambda_function_details['Runtime'] = 'python2.7'
    lambda_function_details['Handler'] = 'service_router.main'

    return lambda_function_details

def get_role():
    """

    :return:
    """
    client = boto3.client('iam')
    roles = client.list_roles()
    print json.dumps(roles, indent=2,default=str)
    role_arn = raw_input('give the role arn you want to give to you lambda function')

    return role_arn

def get_security_group():
    """

    :return:
    """
    client = boto3.client('ec2')
    security_groups = client.describe_security_groups()
    print json.dumps(security_groups,indent=2,default=str)
    security_group = raw_input("security group id  you want to assign to your lambda function")
    return security_group