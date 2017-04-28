import urllib
import os
import yaml

class resourceDescriptor:

    def __init__(self, bucket, filename, savepath):
        self.bucket = bucket
        self.filename = "resourceDescriptors.yaml"
        self.savepath = savepath

    def get_data(self):
        if not os.path.exists(self.savepath):
            print "Making temp file storage: " + self.savepath
            os.makedirs(self.savepath)
        url = "https://github.com/alliance-genome/agr_schemas/blob/master/" + self.bucket + "/" + self.filename
        if not os.path.exists(self.savepath + "/" + self.filename):
            urllib.urlretrieve(url, self.savepath + "/" + self.filename)
        else:
            print "File: " + self.savepath + "/" + self.filename + " already exists not downloading"

        with open(self.savepath + "/" + self.filename, 'r') as stream:
            try:
                print(yaml.load(stream))
            except yaml.YAMLError as exc:
                print(exc)
