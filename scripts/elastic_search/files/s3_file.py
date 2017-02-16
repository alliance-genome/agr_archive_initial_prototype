import boto3
import os

class S3File:

	def __init__(self, bucket, filename):
		self.bucket = bucket
		self.filename = filename
		self.s3 = boto3.client('s3')

	def download(self):
		print "Loading data from s3 (" + self.bucket + "/" + self.filename + ") ..."
		if not os.path.exists("tmp"):
			os.makedirs("tmp")
		self.s3.download_file(self.bucket, self.filename, "tmp/" + self.filename)
		return "tmp/" + self.filename

	def list_files(self):
		pass
