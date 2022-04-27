from flask import Flask
import os 
import sqlite3
from sqlite3 import Error

basedir = os.path.abspath(os.path.dirname(__file__))

parking = Flask(__name__)

parking.config.from_mapping(
	SECRET_KEY = 'who cares',
)

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn

from app import routes