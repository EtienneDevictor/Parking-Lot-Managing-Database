from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import sqlite3
from sqlite3 import Error
import os

app_obj = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

app_obj.config.from_mapping(
	SECRET_KEY = 'who cares',
	# location of the app database
	SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db'),
	SQLALCHEMY_TRACK_MODIFICATIONS = False,
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

conn = create_connection(basedir + "/Parking.db")

from app import routes