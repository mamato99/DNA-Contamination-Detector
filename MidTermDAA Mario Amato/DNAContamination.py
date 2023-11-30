from AVL import AVLTree
from SuffixTree import *


class DNAContamination:

    class Contaminat:

        def __init__(self, sequence, id):
            self.sequence = sequence
            self.id = id


    def __init__(self, stringa,treshold):
        self._stringa = stringa
        self._treshold = treshold
        self._contaminants = AVLTree()
        self._suffix_of_string = SuffixTree((stringa,))

    def addContaminant(self, c):
        lista = self._suffix_of_string._get_all_matched_substring(c.sequence, self._treshold)
        self._contaminants.insert(len(lista), c.id)

    def getContaminants(self, k):
        if k>self._contaminants.len:
            k = self._contaminants.len
        cur = self._contaminants.node_max
        lista = []
        lista.append(cur.data)
        k -= 1
        for i in range(k):
            cur = self._contaminants.before(cur)
            if cur is None:
                break
            lista.append(cur.data)
        return lista





