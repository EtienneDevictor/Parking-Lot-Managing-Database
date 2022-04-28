from sqlalchemy import CheckConstraint, UniqueConstraint


class Permit(db.Model):
    permit_id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    

class Permit_Type(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    days_a_week = db.Column(db.Integer, nullable=False)
    number_of_semesters = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    permit_id = db.column(db.Integer)

class Permit_Holder(db.Model):
    school_id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    phone_number = db.Column(db.Integer)
    email = db.Column(db.String(50), nullable=False)
    type_of_holder = db.Column(db.String(20), nullable=False)
    permit_id = db.Column(db.Integer, nullable=False)


    