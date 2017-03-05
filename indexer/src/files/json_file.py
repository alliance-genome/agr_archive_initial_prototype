import json

class JSONFile:

    def __init__(self, filename):
        self.filename = filename

    def get_data(self):
        print "Loading json data from (" + self.filename + ") ..."
        with open(self.filename, "r") as f:
            data = json.load(f)
        f.close()
        return data
