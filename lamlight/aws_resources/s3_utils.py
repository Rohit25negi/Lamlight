"""
Modules provides the utilities for s3 operations like:
    1) creating new bucket.
    2) uploading file to a bucket.
"""
import ntpath
import os

import boto3


def create_bucket(bucket_name):
    """
    This function creates a new bucket with name 'bucket_name' is
    already not exists.

    Parameters
    -----------
    bucket_name: str
           Name of bucket to be created

    """
    res = boto3.resource("s3")
    my_session = boto3.session.Session()
    my_region = my_session.region_name
    if not my_region:
        my_region = os.getenv('AWS_REGION')

    if res.Bucket(bucket_name) not in res.buckets.all():
        s3_client = boto3.client("s3", region_name=my_region)
        s3_client.create_bucket(Bucket=bucket_name,
                                CreateBucketConfiguration={'LocationConstraint': my_region})


def upload_to_s3(file_path, bucket_name):
    """
    This function uploads a file to the bucket with name 'bucket_name'

    Parameters
    -----------
    file_path: str
           zip file to be uploaded to bucket
    bucket_name: str
           Name of the bucket to which the file is to be uploaded
    file_url: str
           s3 url of the uploaded file.

    """
    s3_client = boto3.client('s3', region_name=os.getenv('AWS_REGION'))
    file_path = os.path.expanduser(file_path)
    file_name = ntpath.basename(file_path)
    s3_client.upload_file(file_path, bucket_name, file_name)
    file_url = '{}/{}/{}'.format(s3_client.meta.endpoint_url,
                                 bucket_name, file_name)
    return file_url
