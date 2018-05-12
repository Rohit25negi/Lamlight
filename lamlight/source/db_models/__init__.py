# This is the initialization module which contains the primitive stuff which
# are needed by the db_models package to work. It contains the following:
# 1. BaseModel : class
#       It is the base class for all the db model that will be going to
#       present in the db_models. This class will serve the purpose
#       of providing the common functionalities.
# 2. db : object that represent the database conenction
#         This object holds the connection to the database. This object should be used
#         throughout the application where the database operation needs to be performed.
#         This object is initialized using DatabaseSession class. This class ensure the
#         single connection to the database.


from db_models.initialize import DatabaseSession


db = DatabaseSession().db_session


class BaseModel(object):
    '''
      It is an abstract class.It is the base class for all the
      db model that will be going to present in the db_models.
      This class will serve the purpose of providing the common
      functionalities.
    '''
    pass
    