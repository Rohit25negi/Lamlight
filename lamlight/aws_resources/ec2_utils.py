"""
Module provides the following utilities:
    1) List the available subnets and let user select one.
    2) List the available IAM roles and let user selecrt one.
    3) List the available Security Groups and let user select one.
"""
import os

import boto3


def get_subnet_id():
    """
    Returns the subnet id for new lambda function

    Returns
    --------
    subnet_id: str
        subnet id
    """
    client = boto3.client('ec2', region_name=os.getenv('AWS_REGION'))
    subnets = client.describe_subnets()
    trimmed_subnets_list = [{"SubnetId": subnet.get("SubnetId"),
                             "VpcId": subnet["VpcId"],
                             "Tags":subnet["Tags"]} for subnet in subnets.get("Subnets")
                            ]
    print "-----------------------------SELECT THE SUBNET---------------------------------"
    for subnet in trimmed_subnets_list:
        print "SUBNET ID = {}".format(subnet["SubnetId"])
        print "VPC ID = {}".format(subnet["VpcId"])
        print "TAGS = {}".format(subnet["Tags"])
        print ""
    print "-------------------------------------------------------------------------------"
    subnet_id = raw_input('enter the subnet id : ').strip()
    return subnet_id


def get_role():
    """
    Returns the IAM role ARN to be assigned to the lambda function

    Returns
    --------
    role_arn: str
            IAM Role ARN
    """
    client = boto3.client('iam', region_name=os.getenv('AWS_REGION'))
    roles = client.list_roles()

    trimed_roles_list = [{'RoleName': role['RoleName'],
                          'Arn': role['Arn']} for role in roles.get('Roles')
                         ]
    print "-----------------------------SELECT THE ROLE----------------------------------"
    for role in trimed_roles_list:
        print "RoleName = {}".format(role.get("RoleName"))
        print "Arn = {}".format(role.get("Arn"))
        print ""
    print "------------------------------------------------------------------------------"
    role_arn = raw_input('give the role Arn : ').strip()

    return role_arn


def get_security_group():
    """
    Returns the Security group id to be assigned to aws lambda function

    Returns
    --------
    security_group: str
        security group id
    """
    client = boto3.client('ec2', region_name=os.getenv('AWS_REGION'))
    security_groups = client.describe_security_groups()
    trimmed_sg_list = [{"GroupName": sg["GroupName"],
                        "GroupId":sg["GroupId"]}
                       for sg in security_groups['SecurityGroups']
                       ]

    print "-----------------------------SELECT THE SECURITY GROUP-------------------------"
    for sec_group in trimmed_sg_list:
        print "GROUP NAME = {}".format(sec_group['GroupName'])
        print "GROUP ID = {}".format(sec_group["GroupId"])
        print ""
    print "--------------------------------------------------------------------------------"
    security_group = raw_input("security group id : ").strip()
    return security_group
