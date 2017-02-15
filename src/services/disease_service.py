from base_controller import BaseController
from dao import DiseaseDAO

class DiseaseController(BaseController):

	def __init__(self):
		self.dao = DiseaseDAO()
