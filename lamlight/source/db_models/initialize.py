

from db_models import db_creds


class DatabaseSession:
    def database_url(self):
        '''
        This function prepares and returns the database url for the
        connection preparation with database.

        '''
        database_user = db_creds.DATABASE_USER
        database_password = db_creds.DATABASE_PASSWORD
        database_host = db_creds.DATABASE_HOST
        database_name = db_creds.DATABASE_NAME

        dsn_tempate = 'dummy_database_url://{usr}:{pass}@{host}/{db_name}'
        format_args = {'usr': database_user,
                       'pass': database_password,
                       'host': database_host,
                       'db_name': database_name
                       }
        db_url = dsn_tempate.format(**format_args)

        return db_url

    def initiate_session(self):
        '''
        This function initializes the database session. This session object
        holds the database connection.
        '''
        db_url = self.database_url()
        #TODO create db connection
        session = None
        return session

    __db_session = None

    def __init__(self):
        if DatabaseSession.__db_session is None:
            session = self.initiate_session()
            DatabaseSession.__db_session = session

    @property
    def db_session(self):
        return DatabaseSession.__db_session