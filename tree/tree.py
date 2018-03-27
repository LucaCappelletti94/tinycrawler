import pickle
from patricia import trie

class Tree:
    default_value = None
    n_of_unparsed = 0
    n_of_parsed = 0

    def __init__(self,filename=None):
        if filename != None:

            with open(filename,"rb") as f:
                self = pickle.load(f)

        self.unparsed_trie = trie()
        self.parsed_trie   = trie()

    def add(self,value):
        self.unparsed_trie[value] = self.default_value
        self.n_of_unparsed += 1

    def pop(self):
        value = self.unparsed_trie.iter("").__next__()
        self.parsed_trie[value] = self.default_value
        self.n_of_unparsed -= 1
        self.n_of_parsed += 1
        return value

    def save(self,filename):
        with open(filename,"a"):
            pass
        with open(filename,"wb") as f:
            pickle.dump(self, f,-1)

    def __contains__(self,value):
        return value in self.unparsed_trie or value in self.parsed_trie
    def __len__(self):
        return self.n_of_unparsed + self.n_of_parsed
