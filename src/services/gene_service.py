from base_service import BaseService
from dao import GeneDAO

class GeneService(BaseService):

	def __init__(self):
		self.dao = GeneDAO()
