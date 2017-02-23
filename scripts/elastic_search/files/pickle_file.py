import pickle

class PickleFile:

    def __init__(self, filename):
        self.filename = filename

    def save(self, objects):
        print "Saving objects into file (" + self.filename + ") ..."
        with open(self.filename, "wb") as f:
            pickle.dump(objects, f, pickle.HIGHEST_PROTOCOL)

    def load(self):
        print "Loading objects from file (" + self.filename + ") ..."
        with open(self.filename, "rb") as f:
            return pickle.load(f)
        return None
