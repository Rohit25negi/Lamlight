import logging
import os
import sys

from distutils.dir_util import copy_tree
import json
import helper as hlpr
import boto3
import zipfile
import ntpath

def create_package(args):
    '''
    It will create the lambda boiler plate. It will perform the following
    tasks:
        1)create the required packages
        2) fill the pacages with the files
        3) entire boiler plate setup has to be created.
    '''
    destination_path = os.getcwd()
    package_path = os.path.dirname(os.path.realpath(__file__))
    source_path = package_path + os.sep + 'source/'
    copy_tree(source_path,destination_path)
    

def update_lamda(lambda_name):
    '''
    '''
    client = boto3.client('lambda')
    lambda_information = client.get_function(FunctionName=lambda_name)
    print lambda_information
    code_location = lambda_information['Code']['Location']
    download_file_path = hlpr.download_object(code_location)
    if hlpr.extract_zipped_code(download_file_path):
        hlpr.save_lamlight_conf(lambda_information)
        print "code downloaded you can start updating your lambda"
    else:
        print "there is some problem extracting ziped file"

    

    
def test_package(args):
    '''
    It will test the lambda boiler plate with the code
    '''
    pass

def deploy_package(args):
    '''
    It will deploy the lambda to s3
    '''
    pass

def build_package():
    '''
    It will build the .zip package after reducing the size
    '''
    command_list = list()
    command_list.append((os.system, "mkdir ./temp_dependencies"))
    command_list.append((os.system,"pip install --upgrade pip"))
    command_list.append((os.system,"pip install  --no-cache-dir -r requirements.txt -t temp_dependencies/"))
    command_list.append((hlpr.remove_test_cases, 'temp_dependencies/'))
    command_list.append((os.system,'cd temp_dependencies/ && zip -r ../.requirements.zip .'))
    command_list.append((os.system, "rm -rf temp_dependencies/ "))
    cwd = os.path.split(os.getcwd())[1]
    command_list.append((os.system,"zip -r ~/{}.zip .".format(cwd)))
    hlpr.run_dependent_commands(command_list)
    return "~/{}.zip".format(cwd)

def push_code():
    account_id =  boto3.client('sts').get_caller_identity().get('Account')
    bucket_name = 'lambda-code-{}'.format(account_id)
    hlpr.create_bucket(bucket_name)
    zip_path = build_package()
    s3_url = hlpr.upload_to_s3(zip_path,bucket_name)
    s3_key = ntpath.basename(zip_path)
    hlpr.link_lambda(bucket_name,s3_key)
    print "done pushing"
