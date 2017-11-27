# This is the automation script which is used to make the lambda package to be
# uploaded on s3

import os
import sys
import shutil

def main(venv):
    os.system("pip install --upgrade pip")
    os.system("pip install  --no-cache-dir -r requirements.txt -t {}/lib/python2.7/site-packages".format(venv))
    os.system('cd {0}/lib/python2.7/site-packages'.format(venv))
    path2 ='{0}/lib/python2.7/site-packages'.format(venv)
    
    for root, dirs, files in os.walk(path2):
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
                    pass

    os.system("cd {}/lib/python2.7/site-packages/ &&  zip -r ../../../../.requirements.zip .".format(venv))
    os.system("rm -r {}".format(venv))
    os.system("zip -r ~/{}.zip .".format(venv))
    print("your code is packed on home with name : {}.zip".format(venv))

if __name__=='__main__':
    main(sys.argv[1])
