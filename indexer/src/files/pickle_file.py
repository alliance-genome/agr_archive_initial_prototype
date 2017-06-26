import cPickle as pickle


class PickleFile:
    def __init__(self, filename):
        self.filename = filename

    def save(self, objects):
        print "Saving objects into file (" + self.filename + ") ..."
        with open(self.filename, "wb") as f:
            pickle.dump(objects, f, pickle.HIGHEST_PROTOCOL)

    def save_append(self, objects):
        print "Appending objects to file (" + self.filename + ") ..."
        with open(self.filename, "ab") as f:
            pickle.dump(objects, f, pickle.HIGHEST_PROTOCOL)

    def load(self):
        print "Loading objects from file (" + self.filename + ") ..."
        with open(self.filename, "rb") as f:
            return pickle.load(f)

    # def load_multi(self):
    #     print "Loading objects from file (" + self.filename + ") ..."
    #     with open(self.filename, "rb") as f:
    #         for _ in range(pickle.load(f)):
    #             yield pickle.load(f)

    def load_multi(self):
        print "Loading objects from file (" + self.filename + ") ..."
        with open(self.filename, "rb") as f:
            while True:
                try:
                    yield pickle.load(f)
                except EOFError:
                    break
