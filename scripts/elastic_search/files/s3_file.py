import boto3
import os

class S3File:

	def __init__(self, bucket, filename, savepath):
		self.bucket = bucket
		self.filename = filename
		self.savepath = savepath
		self.s3 = boto3.client('s3')

	def download(self):
		print "Downloading data from s3 (" + self.bucket + "/" + self.filename + " -> " + self.savepath + "/" + self.filename + ") ..."
		if not os.path.exists(self.savepath):
			os.makedirs(self.savepath)
		self.s3.download_file(self.bucket, self.filename, self.savepath + "/" + self.filename)
		return self.savepath + "/" + self.filename

	def list_files(self):
		pass
