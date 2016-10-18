from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def get_session(db_file):
    """Returns a Sqlalchemy session object for the provided database"""
    return sessionmaker(bind=get_engine(db_file))()

def get_engine(db_file):
    """Returns a Sqlalchemy engine object for the provided database"""
    return create_engine(r'sqlite:///' + db_file)