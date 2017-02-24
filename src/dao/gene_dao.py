from sql_dao import SQLDAO

class GeneDAO(SQLDAO):

    def get(self, gene_id):
        return self.read(GeneModel, gene_id)
