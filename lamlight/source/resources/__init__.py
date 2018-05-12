"""
resources
~~~~~~~~~~
Module defines the Base resource class for other resources
"""


import abc

from abc import abstractmethod


class Resource(object):
    """
    Base resource class
    """
    __metaclass__ = abc.ABCMeta

    @abstractmethod
    def get(self):
        '''
        This is an abstract method.In subclasses this class,
        it acts as the get request on the Resource. This method is
        to be invoked when a get request comes to the resource.

        '''
        pass
    
    @abstractmethod
    def post(self):
        '''
        This is an abstract method.In subclasses this class,
        it acts as the post request on the Resource. This method is
        to be invoked when a post request comes to the resource.

        '''
        pass

    @abstractmethod
    def patch(self):
        '''
        This is an abstract method.In subclasses this class,
        it acts as the patch request on the Resource. This method is
        to be invoked when a patch request comes to the resource.

        '''

        pass
