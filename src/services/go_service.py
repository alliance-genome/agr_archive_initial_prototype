from base_controller import BaseController
from dao import GoDAO

class GoController(BaseController):

	def __init__(self):
		self.dao = GoDAO()
