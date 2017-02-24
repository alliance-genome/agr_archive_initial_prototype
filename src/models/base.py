from app import db

class Base(db.Model):

   __abstract__  = True

   id = db.Column(db.Integer, primary_key=True)
   date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
   date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

   def __repr__(self):
      return "%s(%s)" % ((self.__class__.__name__),
         ', '.join(["%s=%r" % (key, getattr(self, key))
            for key in sorted(self.__dict__.keys())
            if not key.startswith('_')]))
