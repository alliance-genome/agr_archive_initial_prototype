from app import db
from base import Base

class DataEntry(Base):

    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Text)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<DataEntry %r>' % self.name