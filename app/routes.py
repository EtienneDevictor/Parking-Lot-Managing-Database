from app import parking, create_connection, basedir
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
    conn = create_connection(basedir + '/Parking.db')
    cur = conn.cursor()
    rows = list()
    if form.validate_on_submit():
        var = form.criteria.data
        cur.execute(f"""Select p.ID, p.FIRST_NAME, p.LAST_NAME, p.EMAIL, p.TYPE_OF_HOLDER , c.MODEL, c.YEAR, c.COLOR, c.TYPE_OF_CAR, c.LISENCE_PLATE, m.START_DATE, date(m.START_DATE, '+'||t.NUMBER_OF_MONTHS||' month') as END_DATE, t.DAYS_A_WEEK 
                    from PERMIT_HOLDER_TABLE as p 
                    left join CAR_TABLE as c on c.SCHOOL_FK_ID = p.ID
                    left join Permit_Table as m on m.SCHOOL_FK_ID = p.ID
                    left join PERMIT_TYPE_TABLE as t on m.PERMIT_TYPE_FK = t.PERMIT_TYPE_ID
                    where p.id = {str(var)}
                    order by end_date desc""")
        rows = cur.fetchall()
        if len(rows) == 0:
            flash(f'The is no Permit belonging to School Id: {str(var)};')
    return render_template('holder.html', rows=rows, form=form)

@parking.route('/ParkingManager', methods=['GET', 'POST'])
def manager():
    form = IntForm()
    var = 12
    if form.validate_on_submit():
        var = form.criteria.data
    conn = create_connection(basedir + '/Parking.db')
    cur = conn.cursor()
    cur.execute(f"""Select p.Location, p.RESERVED_SLOTS, p.Total_Number_slots, avg(d.total_daily_parking)    
                    from Parking_table as p
                    join daily_parking_table as d on d.location_pk_fk = p.LOCATION
                    where d.date_pk >= date(Current_date, '-{str(var)} month')
                    group by p.LOCATION;""")
    rows = cur.fetchall()
    return render_template('manager.html', rows = rows, form = form)

@parking.route('/MeterMaid', methods=['GET', 'POST'])
def maid():
    form = IntForm()
    var = '0'
    rows = list()
    conn = create_connection(basedir + '/Parking.db')
    cur = conn.cursor()
    if form.validate_on_submit():
        var = form.strCriteria.data
        cur.execute(f"""Select c.Model, c.Year, c.color, c.type_of_car, c.lisence_plate, date(m.START_DATE, '+'||t.NUMBER_OF_MONTHS||' month') as END_DATE
                        from PERMIT_HOLDER_TABLE as p 
                        left join CAR_TABLE as c on c.SCHOOL_FK_ID = p.ID
                        left join Permit_Table as m on m.SCHOOL_FK_ID = p.ID
                        left join PERMIT_TYPE_TABLE as t on m.PERMIT_TYPE_FK = t.PERMIT_TYPE_ID
                        where c.lisence_plate = '{var}' and END_DATE >= CURRENT_DATE
                        order by end_date DESC
                        limit 1;""")
        rows = cur.fetchall()
        if len(rows) == 0:
            flash(f'No permits belong to license plate number {var}')
    return render_template('maid.html', rows=rows, form = form)

@parking.route('/DailyPass', methods=['GET', 'POST'])
def daily():
    form = IntForm()
    rows = list()
    var = 0
    conn = create_connection(basedir + '/Parking.db')
    cur = conn.cursor()
    if form.validate_on_submit():
        var = form.criteria.data
        cur.execute(f"""Select DAY_PASS_ID , DATE_FK as Day, location_fk as location, ARRIVAL_TIME, DEPARTURE_TIME, p.HOURLY_RATE,  p.HOURLY_RATE * (DEPARTURE_TIME - ARRIVAL_TIME) / 100 as Total_Price
                        From DAY_PASS_TABle as d
                        left join Daily_parking_table as dp on d.Location_fk = dp.LOCATION_PK_FK and  d.date_fk = dp.date_pk
                        left join Parking_table as p on p.location = dp.location_pk_fk
                        where DAY_PASS_ID = {str(var)}
                    """)
        rows = cur.fetchall()
        if len(rows) == 0:
                flash(f'There is no daily pass with the id {str(var)}')
    return render_template('daily.html', rows=rows, form = form)