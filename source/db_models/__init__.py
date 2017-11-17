# This is the initialization module which contains the primitive stuff which 
# are needed by the db_models package to work. It contains the following:
# 1. BaseModel : class
#       It is the base class for all the db model that will be going to
#       present in the db_models. This class will serve the purpose
#       of providing the common functionalities.
# 2. session : sqlalchemy Object
#       This reference variable will contain the Session() object after initialization.
#       The session is used to interact with the database. Seperating out the session
#       ensures that multiple session does not form during the execution.

from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base

metadata = MetaData()
session = None


class BaseModel(object):
    '''  
      It is an abstract class.It is the base class for all the 
      db model that will be going to present in the db_models. 
      This class will serve the purpose of providing the common 
      functionalities.
    '''
    __abstract__ = True

    @classmethod
    def get_object(cls,id):
        '''
        This is the factory method which return the object of the class
        whose row is present in the database table with the given id

        PARAMETERS
        ----------
        cls : type
            It is object of current class definition with whose reference
            the method is called.
        id : int|str
            primary key id of the database model whose corresponding
            ORM object is to be returned
        
        RETURNS
        --------
        object:
            Object of BaseModel and/or its subclasses

        '''
        model_obj =  session.query(cls).get(id)
        if model_obj is None:
            raise KeyError(db_err_consts.INVALID_ID.format(cls.__table__))

        return model_obj

    @classmethod
    def get_object_with_ids(cls,ids):
        '''
        This functions returns the list of objects of the db model with the ids
        in the list given.

        PARAMETERS
        ----------
        cls : type
            It is object of current class definition with whose reference
            the method is called.
        ids : list
            list of primary key ids of the database model whose corresponding
            ORM object is to be returned
        
        RETURNS
        --------
        object:
            list of Object of BaseModel and/or its subclasses

        '''
        algo_names = session.query(cls).\
        filter(cls._id.in_(ids)).all()

        return algo_names
    
    def __str__(self):
        return self.__dict__
