from app import db
from base import Base

class DataSet(Base):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    inject_date = db.Column(db.Date)

    def __init__(self, name, inject_date):
        self.name = name
        self.inject_date = inject_date

    def __repr__(self):
        return '<DataSet %r>' % self.name