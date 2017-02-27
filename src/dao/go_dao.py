from elasticsearch_dao import ElasticSearchDAO

class GoDAO(ElasticSearchDAO):

    def __init__(self, db):
        pass

    def get(self, go_id):
        return self.get_by_id(go_id)
