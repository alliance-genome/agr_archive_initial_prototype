import json
import codecs

class JSONFile:

    def get_data(self, filename):
        print "Loading json data from (" + filename + ") ..."
        with codecs.open(filename, 'r', 'UTF-8') as f:
            data = json.load(f)
        f.close()
        return data