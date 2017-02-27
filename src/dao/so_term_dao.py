from sql_dao import SQLDAO

class SoTermDAO(SQLDAO):

    def __init__(self, db):
        pass

    def get(self, so_id):
        return self.read(SoTerm, so_id)
