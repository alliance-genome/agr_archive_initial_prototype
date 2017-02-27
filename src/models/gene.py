from base import Base

class Gene(Base):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
