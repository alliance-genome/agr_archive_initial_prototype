import json

class JSONFile:

    def get_data(self, filename):
        print "Loading json data from (" + filename + ") ..."
        with open(filename, "r") as f:
            data = json.load(f)
        f.close()
        return data
