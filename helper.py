import os
import json
import shutil
import tempfile
import urllib
import zipfile

def run_dependent_commands(command_list):
    for command in command_list:
        assert not command[0](command[1])
    

def remove_test_cases(path):

    for root, dirs, files in os.walk(path):
        path = root.split(os.sep)
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
    temp_dir_path = tempfile.mkdtemp(dir='/tmp')
    download_file_path = temp_dir_path+os.sep+"pet.zip"
    urllib.urlretrieve(url,download_file_path)
    print "file_downloaded"
    return download_file_path


def extract_zipped_code(zipped_code): 
    with zipfile.ZipFile(zipped_code,'r') as zip_ref:
        zip_ref.extractall()
    return True

def save_lamlight_conf(lambda_information):
    conf_file = '.lamlight.conf'
    f = open(conf_file,'w')
    json.dump(lambda_information,f)
