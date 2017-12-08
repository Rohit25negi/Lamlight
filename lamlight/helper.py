"""
This modules provides the helper functions which can be useful throught the project.

"""
import configparser
from distutils.dir_util import copy_tree
import os
import shutil
import tempfile
import urllib
import zipfile

import constants as consts
import errors


def run_dependent_commands(command_list):
    """
    This fucntions executes a list of dependent commands. In which,
    each command is dependent on the success of its previous command.
    If one command fails, remaining commands are not executed.

    Parameters
    -----------
    command_list: list
        list of tuples in which each tuple contains the following content:
            (function_to_execute,arguments_to_pass)

    """
    for command in command_list:
        assert not command[0](*command[1])



def remove_test_cases(path):
    """
    This functions is used to remove the test cases from the heavy
    pip packages.

    Parameters
    -----------
    path : str
        path from where the test cases are to be removed

    Returns
    --------
    int:
        0 if deletion runs successfully. Else, 1.
    """
    for root, dirs, files in os.walk(path):
        for dir in dirs:
            path = root + os.sep + dir
            if os.path.isdir(path) and 'tests' in dir: 
                try:
                    shutil.rmtree(path)
                except Exception:
                    return 1
    return 0


def download_object(url):
    """
    This function is used to download the code package from
    a given url.

    Parameters
    -----------
    url: str
        url from where the object is to be downloaded

    Returns
    --------
    download_file_path: str
            path where the code package is downloaded
    """
    temp_dir_path = tempfile.mkdtemp(dir='/tmp')
    download_file_path = temp_dir_path+os.sep+"pet.zip"
    urllib.urlretrieve(url,download_file_path)
    return download_file_path


def extract_zipped_code(zipped_code):
    """
    This function extracts the zip file in the CWD.

    Parameters
    -----------
    zipped_code: str
           path to zip file which is to be extracted
    """
    with zipfile.ZipFile(zipped_code,'r') as zip_ref:
        zip_ref.extractall()
    

def save_lamlight_conf(lambda_information):
    """
    This functions saves the lambda configuration file to the CWD.
    Lambda cofiguration file contains the information of the lambda
    function to which current project is associated to.

    Parameters
    -----------
    lambda_information: dict
        dictionary which contains the information about a lambda function
    """

    fout = open(consts.LAMLIGHT_CONF,'w')
    conf_parser = configparser.ConfigParser()
    conf_parser.add_section("LAMBDA_FUNCTION")
    conf_parser["LAMBDA_FUNCTION"]["funtionname"] = lambda_information['FunctionName']
    conf_parser.write(fout)

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