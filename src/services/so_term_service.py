from base_service import BaseService
from dao import SoTermDAO

class SoTermService(BaseService):

    def __init__(self, db):
        self.dao = SoTermDAO(db)
