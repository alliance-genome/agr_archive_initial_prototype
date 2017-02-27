from app import db
from base import Base

class Vocabulary(Base):
    __tablename__ = "vocabularies"
    
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String)
    prefix = db.Column(db.String)
