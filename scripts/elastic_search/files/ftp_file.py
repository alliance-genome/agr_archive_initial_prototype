import urllib 
import os

class FTPFile:

    def __init__(self, url, savepath, filename):
        self.url = url
        self.savepath = savepath
        self.filename = filename

    def download(self):
        print "Downloading data from ftp (" + self.url + " -> " + self.savepath + "/" + self.filename + ") ..."
        if not os.path.exists(self.savepath):
            os.makedirs(self.savepath)
        urllib.urlretrieve(self.url, self.savepath + "/" + self.filename)

