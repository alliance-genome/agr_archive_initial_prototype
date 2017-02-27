
class SQLDAO(object):
    
    def __init__(self, db):
        self.db = db
        
    def create(self, object=None):
        """
        Creates new object in the database
        and flushes database changes
        """
        if object:
            self.db.session.add(object)
        self.db.session.flush()

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
            self.db.session.flush()

    def update_all(self, objects=[]):
        """
        Save list of objecst to the database
        flushes database changes
        """
        if objects:
            self.db.session.add_all(objects)
        self.db.session.flush()

    def delete(self, object):
        """
        Delete object from the database
        flushes databases changes
        """
        self.db.sesion.delete(object)
        self.db.session.flush()

