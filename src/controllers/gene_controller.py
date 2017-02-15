from base_controller import BaseController
from dao import GeneDAO

class GeneController(BaseController):

	def __init__(self):
		self.dao = GeneDAO()
