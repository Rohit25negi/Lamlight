import os

import shutil

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

            
