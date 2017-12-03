import traceback

import click

import errors
from  logger import logger
import operations

@click.group()
def cli():
    """
    Lamlight is  python package for serverless application(aws lambda).

    It allows a variety of useful functionalities like:

    1) Create a new aws lambda project.

    2) Building the code package for aws lambda.

    3) Allows to put heavy dependencies like pandas,numpy etc.

    4) Live updating the existing lambda.

    """
    pass


@cli.command()
@click.option('--lambda_name', default='my-project', help='Name of the lambda function')
@click.option('--role', help='IAM Role to be assigned to lambda function')
@click.option('--subnet_id',help='Subnet id to be assigned to lambda function')
@click.option('--security_group',help='Security group to be assigned to lambda function')
def create(name, role, subnet_id, security_group):
    """
    It is used to start with new aws lambda project.
    It will perform the following function:

        1) It creates the aws lambda boilerplate to get started.

        2) It creates a new lamabda function with the name passed. If no\
        name is passed, default name 'my-project' is considered.

    """
    try:
        operations.create_lambda(name, role, subnet_id, security_group)
    except (errors.PackagingError, errors.AWSError,errors.NoLamlightProject) as error:
        logger.error(error.message)
    except Exception as error:
        logger.critical('Unknown error occured.')
        traceback.print_exc()


@cli.command()
@click.option('--lambda_name',required=True,help='Name of the lambda function which is to be updated')
def update(lambda_name):
    """
    It is used to update the existing lambda function. It downloads the code running the given function.
    """
    try:
        operations.update_lamda(lambda_name)
    except (errors.PackagingError, errors.AWSError, errors.NoLamlightProject) as error:
        logger.error(error.message)
    except Exception as error:
        logger.critical('Unknown error occured.')
        traceback.print_exc()

@cli.command()
@click.option('--lambda_name',required=True,help='Name of the lambda function which is to be updated')
def connect(lambda_name):
    """
    It is used to connect your project with an existing lambda function

    """
    try:
        operations.connect_lambda(lambda_name)
    except (errors.PackagingError, errors.AWSError, errors.NoLamlightProject) as error:
        logger.error(error.message)
    except Exception as error:
        logger.critical('Unknown error occured.')
        traceback.print_exc()

@cli.command()
def push():
    """
    It pushes the code of current project to the lambda function which 
    is associated with current project.
    """
    try:
        operations.push_code()
    except (errors.PackagingError, errors.AWSError, errors.NoLamlightProject) as error:
        print error
        logger.error(error.message)
    except Exception as error:
        logger.critical('Unknown error occured.')
        traceback.print_exc()


@cli.command()
@click.option('--type', help='test type (mannual/automatic)', default='automatic')
def test(type):
    """
    This command will be used to test the current project.(Not yet supported)
    """
    logger.error('Not yet supported. But will be soon.')
