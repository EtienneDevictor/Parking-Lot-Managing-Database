import unittest
import os
import sqlite3
from sqlite3 import Error

basedir = os.path.abspath(os.path.dirname(__file__))

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


class TestSum(unittest.TestCase):
    def test_permit_options(self):
         conn = create_connection(basedir + '/Parking.db')
         cur = conn.cursor()
         cur.execute("Select * from PERMIT_TYPE_TABLE;")
         rows = cur.fetchall()
         row = rows[0]
         element = row[0]
         self.assertEqual(element, 10000001, "should be 10000001")
         
    def test_check_permit(self):
        conn = create_connection(basedir + '/Parking.db')
        cur = conn.cursor()
        cur.execute(f"""Select p.ID_PK, p.FIRST_NAME, p.LAST_NAME, p.EMAIL, p.TYPE_OF_HOLDER , c.MODEL, c.YEAR, c.COLOR, c.TYPE_OF_CAR, c.LISENCE_PLATE, m.START_DATE, date(m.START_DATE, '+'||t.NUMBER_OF_MONTHS||' month') as END_DATE, t.DAYS_A_WEEK 
                    from PERMIT_HOLDER_TABLE as p 
                    left join CAR_TABLE as c on c.SCHOOL_FK_ID = p.ID_PK
                    left join Permit_Table as m on m.SCHOOL_FK_ID = p.ID_PK
                    left join PERMIT_TYPE_TABLE as t on m.PERMIT_TYPE_FK = t.PERMIT_TYPE_ID
                    where p.id_pk = 10011
                    order by end_date desc""")
        rows = cur.fetchall()
        row = rows[0]
        element = row[0]
        self.assertEqual(element, 10011, "should be 10011")
        element = row[5]
        self.assertEqual(element,"MERCEDES", "should be MERCEDES" )
        element = row[10]
        self.assertEqual(element, "2022-01-15", "should be 2022-01-15")
        
    def test_parking_manager(self):
         conn = create_connection(basedir + '/Parking.db')
         cur = conn.cursor()
         cur.execute(f"""Select p.Location, p.RESERVED_SLOTS, p.Total_Number_slots, avg(d.total_daily_parking)    
                    from Parking_table as p
                    join daily_parking_table as d on d.location_pk_fk = p.LOCATION
                    where d.date_pk >= date(Current_date, '-2 month')
                    group by p.LOCATION;""")
         rows = cur.fetchall()
         row = rows[0]
         element = row[0]
         self.assertEqual(element, "NORTH", "should be North")
         element = row[3]
         self.assertEqual(element, 95.0, "should be 95.0")
         
    def test_meter_maid(self):
        conn = create_connection(basedir + '/Parking.db')
        cur = conn.cursor()
        cur.execute(f"""Select c.Model, c.Year, c.color, c.type_of_car, c.lisence_plate, date(m.START_DATE, '+'||t.NUMBER_OF_MONTHS||' month') as END_DATE
                        from PERMIT_HOLDER_TABLE as p 
                        left join CAR_TABLE as c on c.SCHOOL_FK_ID = p.ID_PK
                        left join Permit_Table as m on m.SCHOOL_FK_ID = p.ID_PK
                        left join PERMIT_TYPE_TABLE as t on m.PERMIT_TYPE_FK = t.PERMIT_TYPE_ID
                        where c.lisence_plate = '6TRJ244' and END_DATE >= CURRENT_DATE
                        order by end_date DESC
                        limit 1;""")
        rows = cur.fetchall()
        row = rows[0]
        element = row[0]
        self.assertEqual(element, "MAZDA", "should be MAZDA")
        element = row[5]
        self.assertEqual(element, "2022-07-15", "should be 2022-07-15")
        cur.execute(f"""Select c.Model, c.Year, c.color, c.type_of_car, c.lisence_plate, d.Date_FK
                        from DAY_PASS_TABLE as d
                        join Permit_Holder_table as p on p.id_pk = d.SCHOOL_ID_FK
                        Join CAR_TABLE as c on p.id_pk = c.SCHOOL_FK_ID
                        where d.date_fk = '2021-06-17'
                        and c.LISENCE_PLATE = 'FBS1D10' """)
        rows = cur.fetchall()
        row = rows[0]
        element = row[0]
        self.assertEqual(element, "PORSCHE", "should be PORCSHE")
        element = row[5]
        self.assertEqual(element, "2021-06-17", "should be 2021-06-17")
        
    def test_daily_pass(self):
        conn = create_connection(basedir + '/Parking.db')
        cur = conn.cursor()
        cur.execute(f"""Select DAY_PASS_ID , DATE_FK as Day, location_fk as location, ARRIVAL_TIME, DEPARTURE_TIME, p.HOURLY_RATE,  p.HOURLY_RATE * (DEPARTURE_TIME - ARRIVAL_TIME) / 100 as Total_Price
                        From DAY_PASS_TABle as d
                        left join Daily_parking_table as dp on d.Location_fk = dp.LOCATION_PK_FK and  d.date_fk = dp.date_pk
                        left join Parking_table as p on p.location = dp.location_pk_fk
                        where DAY_PASS_ID = 493
                    """)
        rows = cur.fetchall()
        row = rows[0]
        element = row[1]
        self.assertEqual(element, "2021-07-03", "should be 2021-07-03")
        element = row[2]
        self.assertEqual(element, "NORTH", "should be North")
        element = row[6]
        self.assertEqual(element, 114, "Should be 114")
    
        
         
if __name__ == '__main__':
    unittest.main()