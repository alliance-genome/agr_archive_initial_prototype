from loaders import *

if __name__ == '__main__':
    al = AggregateLoader()
    al.establish_index()
    al.load_from_files()
    al.index_mods_from_pickle()
    al.index_data()