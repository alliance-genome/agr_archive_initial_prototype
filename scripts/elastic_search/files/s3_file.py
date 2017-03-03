import urllib 
import os

class S3File:

    def __init__(self, bucket, filename, savepath):
        self.bucket = bucket
        self.filename = filename
        self.savepath = savepath

    def download(self):
        print "Downloading data from s3 (https://s3.amazonaws.com/" + self.bucket + "/" + self.filename + " -> " + self.savepath + "/" + self.filename + ") ..."
        if not os.path.exists(self.savepath):
            print "Making temp file storage: " + self.savepath
            os.makedirs(self.savepath)
        url = "https://s3.amazonaws.com/" + self.bucket + "/" + self.filename
        if not os.path.exists(self.savepath + "/" + self.filename):
            urllib.urlretrieve(url, self.savepath + "/" + self.filename)
        else:
            print "File: " + self.savepath + "/" + self.filename + " already exists not downloading"
        return self.savepath + "/" + self.filename

    def list_files(self):
        pass
