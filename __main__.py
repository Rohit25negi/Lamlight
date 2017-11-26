import operations
import click


@click.group()
def cli():
    """
    Lamlight is developer companion library for serverless application(aws lambda).
    It allows a variety of usefull functions like:
    1) Create a new aws lambda project
    2) Building the code package for aws lambda
    3) Allows to put heavy dependencies like pandas,numpy etc
    4) Live updating the existing lambda
    :return:
    """
    pass


@cli.command()
@click.option('--name', default='my-project', help='Name of the lambda function')
@click.option('--role', help='IAM Role to be assigned to lambda function')
@click.option('--subnet_id',help='Subnet id to be assigned to lambda function')
@click.option('--security_group',help='Security group to be assigned to lambda function')
def create(name, role, subnet_id, security_group):
    """
    It is used to start with new aws lambda project.
    It will perform the following function:

        1) It creates the aws lambda boilerplate to get started.
        2) It creates a new lamabda function with the name passed. If no
           name is passed, default name 'my-project' is considered.

    :param name:
            Name of the lambda function.
    :param role:
            IAM Role to be assigned to lambda function.
    :param subnet_id:
            Subnet id to be assigned to lambda function.
    :param security_group:
            Security group to be assigned to lambda function.
    :return:

    """
    operations.create_lambda(name, role, subnet_id, security_group)


@cli.command()
@click.option('--lambda_name', help='Name of the lambda function which is to be updated')
def update(lambda_name):
    """
    It is used to update the existing lambda function.
    It download the code running the given function.

    :param lambda_name:
            name of the lambda function which is to be updated
    :return:
    """
    print "Downloading your code"
    operations.update_lamda(lambda_name)


@cli.command()
def push():
    """
    It pushes the code of current project to the lambda function  which is
    is associated with current project.
    :return:
    """
    operations.push_code()


@cli.command()
@click.option('--type', help='test type (mannual/automatic)', default='automatic')
def test(type):
    """
    This command will be used to test the current project
    :param type:
    :return:
    """
    #TODO fill this function to test the lambda function code
    pass
