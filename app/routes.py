from app import parking, create_connection, basedir
import app 
import os 
from app.forms import *
from flask import render_template


@parking.route('/')
def home():
    return render_template('home.html')

@parking.route('/PermitOptions')
def options():
    conn = create_connection(basedir + '/Parking.db')
    cur = conn.cursor()
    cur.execute("Select * from PERMIT_TYPE_TABLE;")
    rows = cur.fetchall()
    return render_template('options.html', rows=rows)