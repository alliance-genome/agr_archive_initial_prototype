from base_service import BaseService
from dao import GoDAO

class GoService(BaseService):

	def __init__(self):
		self.dao = GoDAO()
