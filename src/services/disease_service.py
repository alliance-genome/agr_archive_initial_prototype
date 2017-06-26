from base_service import BaseService
from dao import DiseaseDAO

class DiseaseService(BaseService):

    def __init__(self):
        self.dao = DiseaseDAO()
