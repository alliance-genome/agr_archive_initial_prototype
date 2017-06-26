from loaders import *

if __name__ == '__main__':
    al = AggregateLoader()
    al.establish_index()
    al.load_annotations()
    al.load_from_mods(test_set = False)
    al.index_data()