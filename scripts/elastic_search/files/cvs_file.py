
class CVSFile:

	def __init__(self, filename):
		self.filename = filename

	def get_data(self):
		print "Loading cvs data from (" + filename + ") ..."
		with open(filename, "r") as f:
			reader = csv.reader(f, delimiter='\t')
			rows = []
			for row in reader:
				rows.append(row)
		f.close()	
		return rows
