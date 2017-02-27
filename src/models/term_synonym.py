from app import db
from base import Base

class TermSynonym(Base):
    
    __tablename__ = "term_synonyms"

    id = db.Column(db.Integer, primary_key=True)
    vocab_id = db.Column(db.Integer)
    name = db.Column(db.String)
    scope = db.Column(db.String)
