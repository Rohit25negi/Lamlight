'''
lamlight.constants
~~~~~~~~~~~~~~~~~~~
Module contains the constants used in the project.
Module contains the following type of constats
1) error messages
2) console commands
3) logging messages
4) general constatns
'''

LAMLIGHT_CONF = '.lamlight.config'

# error_message
NO_LAMBDA_FUNCTION = " Lambda function with '{}' name does not exist."
SCAFFOLDING_ERROR = 'Could not create project Scaffolding.'
CODE_PULLING_ERROR = "cannot load the code base for '{}' lambda "
PACKAGIN_ERROR = "Could not create the code package."
NO_LAMLIGHT_PROJECT = 'Not a Lamlight project. Get in lamlight by connection to one lambda function'


# console commands
PIP_UPGRADE = "pip install --upgrade pip"
PIP_REQ_INSTALL = "pip install --upgrade --no-cache-dir -r requirements.txt -t temp_dependencies/"
ZIP_DEPENDENCY = 'cd temp_dependencies && zip -r ../.requirements.zip .'


# logger messages
CONNECT_TO_LAMBDA = "Your project is connected to '{}' lambda function"

# general
DEPENDENCY_DIR = '{}/temp_dependencies/'
BUCKET_NAME = 'lambda-code-{}-{}'
