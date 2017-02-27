from app import db
from base import Base

class TermRelationship(Base):
    
    __tablename__ = "term_relationships"

    id = db.Column(db.Integer, primary_key=True)
    vocab_id = db.Column(db.Integer)
    parent_id = db.Column(db.Integer)
    child_id = db.Column(db.Integer)
    relationship_type = db.Column(db.String)
    comment = db.Column(db.String)
