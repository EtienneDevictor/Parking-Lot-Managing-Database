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
    cur.execute("SELECT * FROM tasks")
    rows = cur.fetchall()
    return render_template('options.html', rows=rows)