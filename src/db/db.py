"""Contains helper functions for integrating with Sqlalchemy and MSSQL"""
import pymssql
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def get_session(db_file):
    """Returns a Sqlalchemy session object for the provided database"""
    return sessionmaker(bind=get_engine(db_file))()

def get_engine(db_file):
    """Returns a Sqlalchemy engine object for the provided database"""
    return create_engine(r'sqlite:///' + db_file)

def get_sql_connection(conn_string):
    """
    Returns a pymssql connection object based on the connection string in settings.
    """
    conn_settings = get_conn_settings(conn_string)
    return pymssql.connect(conn_settings['SERVER'], conn_settings['UID'],
                           conn_settings['PWD'], conn_settings['DATABASE'])

def get_conn_settings(conn_string):
    """
    Returns a dictionary of connection settings from a given key=value, ;-delimited connection
    string
    """
    conn_list = [item.split('=') for item in conn_string.split(';')]
    return {item[0]: item[1] for item in conn_list}
