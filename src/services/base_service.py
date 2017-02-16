
class BaseService:

	def get(self, lookup_id):
		return self.dao.get(lookup_id);
