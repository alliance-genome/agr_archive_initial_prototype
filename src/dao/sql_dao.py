from server.app import db

class SQLDAO:
   
   def __init__(self):
      pass
      
   def create(self, object=None):
      """
      Creates new object in the database
      and flushes database changes
      """
      if object:
         db.session.add(object)
      db.session.flush()

   def read(self, model_class, id):
      """
      Reads a object from the database
      """
      return model_class.query.filter("id"==id)

   def update(self, object=None):
      """
      Update all modified sqa objects to the database
      by flushing database changes
      """
      if object:
         db.session.flush()

   def update_all(self, objects=[]):
      """
      Save list of objecst to the database
      flushes database changes
      """
      if objects:
         db.session.add_all(objects)
      db.session.flush()

   def delete(self, object):
      """
      Delete object from the database
      flushes databases changes
      """
      db.sesion.delete(object)
      db.session.flush()

