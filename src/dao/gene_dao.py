from sql_dao import SQLDAO

class GeneDAO(SQLDAO):

    def __init__(self, db):
        super(GeneDAO, self).__init__(db)

    def get(self, gene_id):
        return self.read(GeneModel, gene_id)
