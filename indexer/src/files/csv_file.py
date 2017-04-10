from comment_file import CommentFile
import csv

class CSVFile:

    def __init__(self, filename):
        self.filename = filename

    def get_data(self):
        print "Loading csv data from (" + self.filename + ") ..."
        with open(self.filename, "r") as f:
            reader = csv.reader(CommentFile(f), delimiter='\t')
            rows = []
            for row in reader:
                rows.append(row)
        f.close()    
        return rows
