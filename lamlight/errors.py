"""
lamlight.errors
~~~~~~~~~~~~~~~~
This modules defines the custom exceptions
"""


class BaseException(Exception):
    """
    Class is the base exception class for expected Exceptions that can rise while
    using lamlight
    """
    def __init__(self, *args, **kwargs):
        """
        Constructor
        """
        super(BaseException, self).__init__(*args, **kwargs)

    def __str__(self):
        return self.message


class NoLamlightProject(BaseException):
    """
    Class defines the Exception raise when lamlight is used in a non-lamlight project
    """
    def __init__(self, *args, **kwargs):
        """
        Constructor
        """
        super(NoLamlightProject, self).__init__(*args, **kwargs)


class AWSError(BaseException):
    """
    Class defines the exception raise when there is some AWS error
    """
    def __init__(self, *args, **kwargs):
        """
        COnstructor
        """
        super(AWSError, self).__init__(*args, **kwargs)


class PackagingError(BaseException):
    """
    Class signifies the Exceptions raised while building the package
    """
    def __init__(self, *args, **kwargs):
        """
        Constructor
        """
        super(PackagingError, self).__init__(*args, **kwargs)
