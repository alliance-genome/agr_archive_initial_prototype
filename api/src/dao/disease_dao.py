from elasticsearch_dao import ElasticSearchDAO

class DiseaseDAO(ElasticSearchDAO):

    def get(self, gene_id):
        return self.get_by_id(gene_id)
