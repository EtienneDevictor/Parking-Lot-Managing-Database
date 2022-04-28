from app import app_obj, create_connection, basedir
import app
from app.forms import *
from flask import render_template, escape, flash, redirect, session, request

@app_obj.route('/')
def home():
    return render_template('home.html')

@app_obj.route('/Manager')
def manager():
    return render_template('manager.html')

@app_obj.route('/PermitHolder')
def holder():
    form = PermitHolderForm()
    return render_template('holder.html', form = form)

@app_obj.route('/PermitOption')
def option():
    conn = create_connection(basedir + "/Parking.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM Permit_Type") 
    rows = cur.fetchall()
    return render_template('option.html', rows = rows)

@app_obj.route('/MeterMaid')
def maid():
    return render_template('maid.html')

