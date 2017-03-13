from app import db
from base import Base

class DataProvider(Base):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<DataProvider %r>' % self.name