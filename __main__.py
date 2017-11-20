import argparse
import sys

import operations
import click


@click.group()
def cli():
    pass


@cli.command()
@click.option('--name', default='my-project', help='asdfa')
@click.option('--s3_bucket', help='asdfa')
@click.option('--lambda_arn', help='asdfa')
def create(name, s3_bucket, lambda_arn):
    print name
    print s3_bucket
    print lambda_arn
    operations.create_package(None)


@cli.command()
@click.option('--lambda_name', help='lambda function name')
def update(lambda_name):
    operations.update_lamda(lambda_name)


@cli.command()
def push():
    operations.push_code()
    


@cli.command()
@click.option('--type', help='test type (mannual/automatic)', default='automatic')
def test(type):
    print "project will be build"
