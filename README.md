## Lamlight

**lamlight** is a python package for serverless application. It abstracts out all the steps needed to develop a servless application for _AWS lambda_. It cuts down 90% of time for deploying/updating AWS lambda. 

[![license](https://docs.google.com/uc?id=1P6tdP072hh890fovxgnk3ZFsWX-QMIfu)](https://www.linkedin.com/in/rohit25negi/)

### Contents
* [Problems/Issues Solved](#problem-focused)
* [Features](#features)
* [Prerequisite](#prerequisite)
* [Quick Start](#quick-start)
* [Examples](#examples)

### Problem focused
Faster, better and robust delivery is becoming crucial. This is where microservices and serverless apps shine. Along, with the huge advantage of using microservices there are some limitation that cloud platforms like [AWS](https://docs.aws.amazon.com/lambda/latest/dg/limits.html) applies. **Lamlight** is made to solve these issues for all developers out there. You just need to write the code and leave everything else on  **Lamlight**.

The problems/issues focused on:
* **Putting large size dependencies on aws lambda(will be for other platforms also soon)**: AWS lambda imposes a limit of 250 MB on code/dependencies size. So, How to use large dependencies like numpy, pandas, scipy on aws lambda? Simple, use  **Lamlight**.  Lamlight compresses the package to its extent and allows you put the dependencies of size of almost 600 MBs.
* **One click deployment**: **Lamlight** works like GIT for you. Just connect with a lambda function once and push the code everytime with a single command.
* **Updating existing code**: Checking the existing code deployed on AWS lambda function is very useful for debbuging and making quick patches. Lamlight made it very simple for you.
* **push to multiple places**: Code you have worked on can be very easily pushed to differnt AWS lambdas, Just connect with a new AWS lambda function you want(similar to changing the remote in GIT) and push.

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
2. **Create lamlight project**
    ```
    lamlight create \
    --lambda_name demo_lambda \
    --role arn:aws:iam::<accountid>:role/<role_name>\
    --subnet_id subnet-<subnet_id>\
    --security_group sg-<sg_id>
    ```
3. **Push the code to lambda**
    ```
    lamlight push
    ```

### Example
1. **Connect with existing AWS lambda function**
```
~$ cd my_project
my_project/$ lamlight connect --lambda_name my_lambda
my_project/$ lamlight push

```

# Made with  ![alt text](https://docs.google.com/uc?id=1KtBi0X2fSN04XpS62T1s2sMeWxXj60Pj)
