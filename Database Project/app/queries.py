def potential_permit_holder(conn):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    
    cur = conn.cursor()
    cur.execute("SELECT * FROM tasks") 

    rows = cur.fetchall()
    
    return rows