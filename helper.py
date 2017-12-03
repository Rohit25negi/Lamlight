import configparser
import json
import ntpath
import os
import shutil
import tempfile
import urllib
import zipfile

import boto3
from botocore.exceptions import ClientError

import constants as consts
import errors


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


def lambda_function_exists(name):
    try:
        client = boto3.client('lambda')
        client.get_function(FunctionName=name)
        return True
    except Exception:
        return False

def remove_test_cases(path):
    """
    This functions is used to remove the test cases from the heavy
    pip packages.
    :param path:
           path from which the test cases are to be removed
    :return:
    """
    for root, dirs, files in os.walk(path):
        for dir in dirs:
            path=root+os.sep+dir
            
            if os.path.isdir(path) and 'tests' in dir: 
                try:
                    shutil.rmtree(path)
                except Exception as err:
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
    

def save_lamlight_conf(lambda_information):
    """
    This functions saves the lambda configuration file to the CWD.
    Lambda cofiguration file contains the information of the lambda
    function to which current project is associated to.

    :param lambda_information:
    :return:
    """

    fout = open(consts.LAMLIGHT_CONF,'w')
    conf_parser = configparser.ConfigParser()
    conf_parser.add_section("LAMBDA_FUNCTION")
    conf_parser["LAMBDA_FUNCTION"]["funtionname"] = lambda_information['FunctionName']
    conf_parser.write(fout)


def create_bucket(bucket_name):
    """
    This function creates a new bucket with name 'bucket_name' is
    already not exists.

    :param bucket_name:
           Name of bucket to be created
    :return:

    """
    res = boto3.resource("s3")
    my_session = boto3.session.Session()
    my_region = my_session.region_name
    if res.Bucket(bucket_name) not in res.buckets.all():
        s3 = boto3.client("s3")
        s3.create_bucket(Bucket=bucket_name,CreateBucketConfiguration={
        'LocationConstraint': my_region})


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
    s3.upload_file(zip_path,bucket_name,file_name)
    file_url = '%s/%s/%s' % (s3.meta.endpoint_url, bucket_name, file_name)
    return file_url

def link_lambda(bucket_name, s3_key):
    """
    It links the code package on s3 bucket to the lambda function.
    :param bucket_name:
           Name of the bucket where the code package is present
    :param s3_key:
           Key of the code package
    :return:
    """
    client = boto3.client('lambda')
    parser = configparser.ConfigParser()
    parser.read(consts.LAMLIGHT_CONF)
    client.update_function_code(FunctionName=parser['LAMBDA_FUNTION']['funtionname'],
                                S3Bucket=bucket_name, S3Key=s3_key)


def create_lambda_function(name, role, subnet_id, security_group, zip_path):
    """
    This function creates the lambda function with the given information
    passed as the arguments.

    :param name:
            Name of the lambda function
    :param role:
            IAM Role to be assigned to the lambda function
    :param subnet_id:
            Subnet to be assgined to the lambda function
    :param security_group:
            Security group to be assigned to the lambda function
    :param zip_path:
            zip path which contains the code to be uploaded on lambda function
    :return:
    """
    try:
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
    
        return lambda_info
    except Exception as error:
        raise errors.AWSError(error.message)


def get_subnet_id():
    """
    Returns the subnet id for new lambda function

    :return subnet_id:
        subnet id
    """
    client = boto3.client('ec2')
    subnets = client.describe_subnets()
    trimmed_subnets_list = [{"SubnetId":subnet.get("SubnetId"),
                                 "VpcId":subnet["VpcId"],
                                 "Tags":subnet["Tags"]}
                                for subnet in subnets.get("Subnets")]
    print "-----------------------------SELECT THE SUBNET---------------------------------"
    for subnet in trimmed_subnets_list:
        print "SUBNET ID = {}".format(subnet["SubnetId"])
        print "VPC ID = {}".format(subnet["VpcId"])
        print "TAGS = {}".format(subnet["Tags"])
        print ""
    print "-------------------------------------------------------------------------------"
    subnet_id = raw_input('enter the subnet id : ').strip()
    return subnet_id
        


def default_lambda_details():
    """
    Returns the default lambda details.

    :return lambda_function_details:
        default lambda function details for python2.7
    """

    lambda_function_details = dict()
    lambda_function_details['Runtime'] = 'python2.7'
    lambda_function_details['Handler'] = 'service_router.main'

    return lambda_function_details


def get_role():
    """
    Returns the IAM role ARN to be assigned to the lambda function

    :return role_arn:
            IAM Role ARN
    """
    client = boto3.client('iam')
    roles = client.list_roles()

    trimed_roles_list = [{'RoleName':role['RoleName'],'Arn':role['Arn']} for role in roles.get('Roles')]
    print "-----------------------------SELECT THE ROLE----------------------------------"
    for role in trimed_roles_list:
        print "RoleName = {}".format(role.get("RoleName"))
        print "Arn = {}".format(role.get("Arn"))
        print ""
    print "------------------------------------------------------------------------------"
    role_arn = raw_input('give the role Arn : ').strip()

    return role_arn


def get_security_group():
    """
    Returns the Security group id to be assigned to aws lambda function

    :return security_group:
        security group id
    """
    client = boto3.client('ec2')
    security_groups = client.describe_security_groups()
    trimmed_sg_list = [{"GroupName":sg["GroupName"],
                        "GroupId":sg["GroupId"]}
                       for sg in security_groups['SecurityGroups']]

    print "-----------------------------SELECT THE SECURITY GROUP-------------------------"
    for sg in trimmed_sg_list:
        print "GROUP NAME = {}".format(sg['GroupName'])
        print "GROUP ID = {}".format(sg["GroupId"])
        print ""
    print "--------------------------------------------------------------------------------"
    security_group = raw_input("security group id : ").strip()
    return security_group
