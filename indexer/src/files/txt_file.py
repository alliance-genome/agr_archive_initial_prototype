
class TXTFile:

    def __init__(self, filename):
        self.filename = filename

    def get_data(self):
        print "Loading txt data from (" + self.filename + ") ..."
        lines = []
        with open(self.filename, "r") as f:
            for line in f:
                lines.append(line)
        f.close()    
        return lines
