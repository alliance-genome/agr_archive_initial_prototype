from comment_file import CommentFile
import csv
import codecs

class CSVFile:

    def __init__(self, filename):
        self.filename = filename

    def get_data(self):
        print "Loading csv data from (" + self.filename + ") ..."
        with codecs.open(self.filename, 'r', 'utf-8') as f:
            reader = csv.reader(CommentFile(f), delimiter='\t')
            rows = []
            for row in reader:
                rows.append(row)
        f.close()    
        return rows
