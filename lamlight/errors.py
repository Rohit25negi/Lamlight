"""
This modules defines the custom exceptions
"""


class BaseException(Exception):

    def __init__(self, *args, **kwargs):
        super(BaseException, self).__init__(*args, **kwargs)

    def __str__(self):
        return self.message


class NoLamlightProject(BaseException):
    def __init__(self, *args, **kwargs):
        super(NoLamlightProject, self).__init__(*args, **kwargs)


class AWSError(BaseException):
    def __init__(self, *args, **kwargs):
        super(AWSError, self).__init__(*args, **kwargs)


class PackagingError(BaseException):
    def __init__(self, *args, **kwargs):
        super(PackagingError, self).__init__(*args, **kwargs)
