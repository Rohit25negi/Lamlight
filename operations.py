import logging
import os
import sys

from distutils.dir_util import copy_tree

import helper as hlpr


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

def build_package(args):
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
