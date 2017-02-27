from app import db
from base import Base

class Term(Base):
    
    __tablename__ = "terms"

    id = db.Column(db.Integer, primary_key=True)
    vocab_id = db.Column(db.Integer)
    name = db.Column(db.String)
    definition = db.Column(db.String)
