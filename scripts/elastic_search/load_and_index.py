from loaders import *

if __name__ == '__main__':
    al = AggregateLoader()
    al.load_from_files()
    al.index_data()
