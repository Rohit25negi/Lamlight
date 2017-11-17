import argparse
import sys

import operations
import click


@click.group()
def cli():
    pass


@cli.command()
def create():
    print "project will be created"


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
    opr_list["build"] = operations.build_package
    opr_list["push"] = operations.deploy_package
    return opr_list

if __name__ =='__main__':
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()

    group.add_argument("--create",help='create a new lambda project')
    group.add_argument("--build",help='build the project')
    group.add_argument("--test",help='test the project locally')
    group.add_argument("--deploy",help='deploy the project')
    
    parser.parse_args()
    main({"opr":sys.argv[1],"args":sys.argv[2]})
