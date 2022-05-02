from app import parking, create_connection, basedir
import app 
import os 
from app.forms import *
from flask import flash, render_template


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

@parking.route('/PermitHolder' , methods=['GET', 'POST'])
def holder():
    form = IntForm()
    var = '-1'
    if form.validate_on_submit():
        var = form.criteria.data
    conn = create_connection(basedir + '/Parking.db')
    cur = conn.cursor()
    cur.execute(f"""Select p.ID, p.FIRST_NAME, p.LAST_NAME, p.EMAIL, p.TYPE_OF_HOLDER , c.MODEL, c.YEAR, c.COLOR, c.TYPE_OF_CAR, c.LISENCE_PLATE, m.START_DATE, date(m.START_DATE, '+'||t.NUMBER_OF_MONTHS||' month') as END_DATE, t.DAYS_A_WEEK 
                    from PERMIT_HOLDER_TABLE as p 
                    left join CAR_TABLE as c on c.SCHOOL_FK_ID = p.ID
                    left join Permit_Table as m on m.SCHOOL_FK_ID = p.ID
                    left join PERMIT_TYPE_TABLE as t on m.PERMIT_TYPE_FK = t.PERMIT_TYPE_ID
                    where p.id = {str(var)}
                    order by end_date desc""")
    rows = cur.fetchall()
    return render_template('holder.html', rows=rows, form=form)

@parking.route('/ParkingManager', methods=['GET', 'POST'])
def manager():
    form = IntForm()
    conn = create_connection(basedir + '/Parking.db')
    cur = conn.cursor()
    cur.execute("""Select p.Location, p.RESERVED_SLOTS, p.Total_Number_slots, avg(d.total_daily_parking)    
                    from Parking_table as p
                    join daily_parking_table as d on d.location_pk_fk = p.LOCATION
                    where d.date_pk >= Current_date - '6 month'
                    group by p.LOCATION;""")
    rows = cur.fetchall()
    return render_template('manager.html', rows = rows, form = form)

@parking.route('/MeterMaid', methods=['GET', 'POST'])
def maid():
    form = IntForm()
    conn = create_connection(basedir + '/Parking.db')
    cur = conn.cursor()
    cur.execute("""Select c.Model, c.Year, c.color, c.type_of_car, c.lisence_plate, date(m.START_DATE, '+'||t.NUMBER_OF_MONTHS||' month') as END_DATE
                        from PERMIT_HOLDER_TABLE as p 
                        left join CAR_TABLE as c on c.SCHOOL_FK_ID = p.ID
                        left join Permit_Table as m on m.SCHOOL_FK_ID = p.ID
                        left join PERMIT_TYPE_TABLE as t on m.PERMIT_TYPE_FK = t.PERMIT_TYPE_ID
                        where c.lisence_plate = '6TRJ244' and END_DATE >= CURRENT_DATE
                        order by end_date DESC
                        limit 1;""")
    rows = cur.fetchall()
    return render_template('maid.html', rows=rows, form = form)

@parking.route('/DailyPass', methods=['GET', 'POST'])
def daily():
    form = IntForm()
    conn = create_connection(basedir + '/Parking.db')
    cur = conn.cursor()
    cur.execute("""Select DAY_PASS_ID , DATE_FK as Day, location_fk as location, ARRIVAL_TIME, DEPARTURE_TIME, HOURLY_RATE,  HOURLY_RATE * (DEPARTURE_TIME - ARRIVAL_TIME) / 100 as Total_Price
                        From DAY_PASS_TABLE
                        where DAY_PASS_ID = 21
                    """)
    rows = cur.fetchall()
    return render_template('daily.html', rows=rows, form = form)