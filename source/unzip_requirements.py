# This is the module which is used to extract all the pip dependencies before
# any execution of the lambda function code. This module is added to bypass the
# lambda function memory constraint. Code mentioned below executes as soon as
# programmer imports this file.

import os
import sys
import zipfile

import constants as consts
import logger

def extract_dependencies():
    '''
        This function is used to extract the pip dependencies to /tmp/dependencies
        folder. '.requirements.zip' file is taken as the extraction source.
        If unziping is done successfully then confirmation message is given. Else,
        Error is thrown.        
    '''
    requirements = '.requirements.zip'

    if  os.system("unzip {} -d {}".format(requirements, consts.DEPENDENCIES_PATH)):
        raise Exception(consts.UNZIP_ERROR)
    else:
        MARKER_UNZIP = consts.MARKER_UNZIP_MSG
        logger.log_to_cloudwatch(MARKER_UNZIP, "done with extracting dependencies")

if not os.path.isdir(consts.DEPENDENCIES_PATH):
    extract_dependencies()

sys.path.append(consts.DEPENDENCIES_PATH)
