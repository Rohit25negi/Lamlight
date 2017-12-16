**lamlight** is a python package for serverless application. It abstracts out all the steps needed to develop a servless application for _AWS lambda_. It cuts down 90% of time for deploying/updating AWS lambda. 


### Contents
* [Features](#Features)
* [Prerequisite](#Prerequisite)
* [Quick Start](#Quick-Start)

### Features
* Creating _boilerplate_ for AWS lambda function.
* Live _upading_ existing AWS lambda function.
* _Connecting_ existing project to AWS lambda function.
* Single command to _push_ code to lambda function.

### Prerequisite
* python 2.7
* pip 
* Add your aws credentials in `~/.aws/credentials` or if you are using IAM roles then set `AWS_REGION` for default AWS region


### Quick Start
1. **Install the Package**
    ```
    pip install git+https://github.com/Rohit25negi/lamlight
    ```
2. **Make project Directory**
    ```
    mkdir demo_project
    ```
3. **Get into the project**
    ```
    cd demo_project
    ```
4. **Create lamlight project**
    ```
    lamlight create \
    --lambda_name demo_lambda \
    --role arn:aws:iam::<accountid>:role/<role_name>\
    --subnet_id subnet-<subnet_id>\
    --security_group sg-<sg_id>
    ```
5. **Push the code to lambda**
    ```
    lamblight push
    ```
