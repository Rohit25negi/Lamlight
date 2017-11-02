import sys

import operations

def main(args):
    operation = args['opr']
    arguments = args['args']


    opr_list = opers()
    if operation in opr_list:
        opr_list[operation](arguments)
    else:
        print "invalid operation :" + operation



def opers():
    opr_list = {}
    opr_list["create"] = operations.create_package
    opr_list["test"] = operations.test_package
    opr_list["push"] = operations.deploy_package
    return opr_list

if __name__ =='__main__':
    main({"opr":sys.argv[1],"args":sys.argv[2]})