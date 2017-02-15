import fnmatch

class JsonFile:

	def __init__(self, filename):
		self.filename = filename

	def get_data(self):
		print "Loading json data from (" + filename + ") ..."
		with open(filename, "r") as f:
			data = json.load(f)
		f.close()
		return data