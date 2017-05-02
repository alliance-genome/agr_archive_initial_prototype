import codecs

class TXTFile:

    def __init__(self, filename):
        self.filename = filename

    def get_data(self):
        print "Loading txt data from (" + self.filename + ") ..."
        lines = []
        with codecs.open(self.filename, 'r', 'utf-8') as f:
            for line in f:
                lines.append(line)
        f.close()    
        return lines