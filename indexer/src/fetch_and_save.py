from loaders import *

if __name__ == '__main__':
    al = AggregateLoader()
    al.load_annotations()
    al.load_from_mods(pickle = 'true', index = 'false')
    al.save_to_files()