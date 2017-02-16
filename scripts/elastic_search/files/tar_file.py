import tarfile

class TARFile:

	def __init__(self, path, tarfilename):
		self.path = path
		self.tarfilename = tarfilename

	def extract_all(self):
		print "Extracting files from (" + self.path + "/" + self.tarfilename + ") ..."

		tfile = tarfile.open(self.path + "/" + self.tarfilename, 'r')
		for member in tfile.getmembers():
			print "Extracting (" + member.name + " -> " + self.path + "/" + member.name + ")"
		tfile.extractall(self.path)
