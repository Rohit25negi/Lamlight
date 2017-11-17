from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db_models import db_creds 
import db_models as db_session
from workflow import workflow_model


def initiate_session():
    '''
    This function initializes the database session. This session is the
    object of Session() which acts a session factory to get the session(connection)
    with the database. 
    '''
    db_url = database_url()
    engine = create_engine(db_url)
    Session = sessionmaker(bind=engine)
    db_session.session = Session()
    return db_session.session

def database_url():
    '''
    This function prepares and returns the databas url for the
    connection preparation with the postgres database using sqlalchemy.
    
    '''
    database_user = db_creds.DATABASE_USER
    database_password = db_creds.DATABASE_PASSWORD
    database_host = db_creds.DATABASE_HOST
    database_name = db_creds.DATABASE_NAME
    
    dsn_tempate = 'postgresql+psycopg2://{usr}:{pass}@{host}/{db_name}'
    format_args = {'usr':database_user,
                   'pass':database_password,
                   'host':database_host,
                   'db_name':database_name
                  }
    db_url = dsn_tempate.format(**format_args)

    return db_url