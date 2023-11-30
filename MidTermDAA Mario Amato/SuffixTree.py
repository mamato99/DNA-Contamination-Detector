
import string


class SuffixTree:
    class _Nodo:
        def __init__(self, parent=None, identifier=None, start=None, stop=None):
            self._parent = parent
            self._children = {}
            self._markers = []
            self._identifier = identifier
            self._start = start
            self._stop = stop
            self._depth = 0

        def _add_markers(self, index: int):
            if index not in self._markers:
                self._markers.append(index)

        def _update_parent_of_children(self, new_parent):
            for i in self._children:
                self._children[i]._parent = new_parent

    class Position:

        def __init__(self, container, node):
            self._container = container
            self._node = node

        def get_node(self):
            return self._node

        def get_container(self):
            return self._container

        def __eq__(self, other):
            return type(other) is type(self) and other.get_node() is self._node

        def __ne__(self, other):
            return not (self == other)

    # ----------------METODI POSITION IN SUFFIX TREE-----------------#
    def _validate(self, p):

        if not isinstance(p, self.Position):
            raise TypeError('The object passed is not a position')
        if p.get_container() is not self:
            raise ValueError('The position passed is not part of this suffix tree')
        return p.get_node()

    def _make_position(self, node):
        return self.Position(self, node) if node is not None else None

    def __init__(self, S):
        self._root = self._Nodo()
        self._tuple = S
        self._create_Suffix(self._tuple)

    # ----------------METODI PRIVATI IN SUFFIX TREE-----------------#

    def _get_label_index_to_string(self, index, start, stop, no_children: bool):
        """
        :param index: identifier of the string
        :param start: index where the label starts
        :param stop: index where the label stops
        :param no_children: boolean that indicates if the node with this label has or not children
        :return: the string between the index start and stop
        """
        label = self._tuple[index]
        len_label = len(label)

        if start == len_label and stop == len_label:
            if no_children:
                return "$"
            else:
                return label[len_label - 1]
        if stop == len_label:
            if no_children:
                label += "$"
                return label[start:]
            else:
                return label[start:]

        return label[start:stop]

    def _has_child(self, node):
        return len(node._children) > 0

    def _longest_common_prefix(self, s1: string, s2: string):
        match = 0
        for t in range(len(s1)):
            if s1[t] == s2[t]:
                match += 1
            else:
                break
            if len(s1) - match == 0 or len(s2) - match == 0:
                return match
        return match

    def _add_markers_to_nodes(self, node_parent, node_son, new_marker):
        """
       This private method updates the parent's markers, which it takes as input,
       with the new marker and copies the parent's markers to the child
        :param node_parent: parent from which the markers are copied
        :param node_son: children in which the markers are copied
        :param new_marker: new marker that must be added to the parent
        :return: returns the reference to the child node
        """
        for i in node_parent._markers:
            node_son._add_markers(i)

        node_parent._add_markers(new_marker)

        return node_son

    
    def _node_split(self, node, new_node_string, matching_index, marker, curr_index):
        """
        This private method restructures the node after a partial
        match has occurred internally and updates its children and parent.
        :param node: the node where the partial match occurr
        :param new_node_string: the new string that has not be matched
        :param matching_index: the match that was found
        :param marker: marker of the current node
        :param curr_index: current string indexes
        :return: return the reference to the node
        """
        old_start = node._start
        old_stop = node._stop

        new_node = self._Nodo(node, node._identifier, old_start + matching_index, old_stop)
        new_node._depth = new_node._parent._depth

        "this method updates the parent of the children by setting it to the new node"
        node._update_parent_of_children(new_node)

        new_node._children = node._children
        new_node = self._add_markers_to_nodes(node, new_node, marker)

        node._children = {}
        node._children.__setitem__(new_node_string[0], new_node)
        node._depth = node._parent._depth + (node._stop - node._start)

        "I update the indeces of the node"
        if marker == node._identifier:
            node._start = curr_index
            node._stop = curr_index + matching_index
        else:
            node._start = old_start
            node._stop = old_start + matching_index
        return node


    def _create_Suffix(self, tuple):
        """
        This private method creates the suffix tree of the tuple passed as input
        :param tuple: string tuple to be transformed into suffix tree
        :return: 
        """

        for j in range(len(tuple)):
            stringa = tuple[j]
            len_stringa = len(stringa)
            stringa += '$'
            match = 0

            for i in range(len(stringa) - 2, -1, -1):

                cur = self._root
                to_ins = stringa[i:]

                if to_ins[0] not in cur._children:
                    node = self._Nodo(cur, j, i, len_stringa)
                    node._depth = node._stop - node._start  
                    node._add_markers(j)
                    cur._children.__setitem__(to_ins[0], node)
                else:
                    curr_index = i  # mi salvo l'indice corrente
                    num_of_descent = 0  #questo numero mi indica quante volte sono sceso nei figli
                    total_matched = 0
                    while to_ins[0] in cur._children:
                        if num_of_descent > 0:
                            curr_index += match  #se sono già sceso una volta nei figli devo aggiornare l'indice corrente
                        cur = cur._children.get(to_ins[0]) #mi sposto nel figlio trovato
                        cur_label = self._get_label_index_to_string(cur._identifier, cur._start, cur._stop,
                                                    len(cur._children) == 0)
                        match = self._longest_common_prefix(cur_label, to_ins)
                        total_matched += match

                        if match < len(cur_label): #è avvenuto un match parziale nel nodo e quindi ho bisogno di ristrutturare
                            cur = self._node_split(cur, cur_label[match:], match, j, curr_index)
                        else:
                            cur._add_markers(j)
                            if cur._identifier == j:
                                cur._start = curr_index
                                cur._stop = curr_index + match

                        to_ins = to_ins[match:]
                        num_of_descent += 1  #
                        if len(to_ins) <= 0:
                            break

                    if len(to_ins) > 0:
                        if cur._identifier == j:
                            node = self._Nodo(cur, j, cur._stop, len_stringa)
                            node._add_markers(j)
                            node._depth = node._parent._depth + (node._stop - node._start)
                            cur._children.__setitem__(to_ins[0], node)
                        else:
                            node = self._Nodo(cur, j, i + total_matched, len_stringa)
                            node._add_markers(j)
                            node._depth = node._parent._depth + (node._stop - node._start)
                            cur._children.__setitem__(to_ins[0], node)



    def _match_between_strings(self, sequence, treshold):
        """
        This private method counts all the matches within the tree with the given string
        and returns the cut string if this is greater than the treshold otherwise null
        :param sequence: sequence that must be compared with the Suffix Tree
        :param treshold: limit after which we take the strings
        :return: none if the string is smallest than the treshold otherwise the string
        """
        str = sequence
        cur = self._root
        total_matched = 0
        if str[0] not in self._root._children:
            return ""
        else:
            while str[0] in cur._children:
                cur = cur._children.get(str[0])
                cur_label = self._get_label_index_to_string(cur._identifier, cur._start, cur._stop, len(cur._children) == 0)
                match = self._longest_common_prefix(cur_label, str)
                total_matched += match
                str = str[match:]
                if len(str) == 0 or match<len(cur_label):
                    break

            ret_str = sequence[:total_matched]

            if len(ret_str) < treshold:
                return None
            else:
                return ret_str


    def _get_all_matched_substring(self, sequence, treshold):
        """
        This private method returns a list with all sub sequences that are greater than or equal to the treshold 
        :param sequence: sequence of the contaminant
        :param treshold: limits after which I consider substrings
        :return: a list of tuple in which i have: the string of contaminant, the start index and the stop index 
        """""
        i = 0
        lista = []
        while i < len(sequence):

            common_str = self._match_between_strings(sequence[i:], treshold)
            if common_str is not None:
                tuple_to_ins = (common_str, i, i+len(common_str)-1)
                num_of_descent = 0
                for j in lista:
                   if tuple_to_ins[1] >= j[1] and tuple_to_ins[2] <= j[2]:
                       num_of_descent = 1
                       break

                if num_of_descent == 0:
                    lista.append(tuple_to_ins)


            i += 1

        return lista

    def getNodeLabel(self, P):
        """
        This public method returns the substring that labels the node of T to which
        position P refers
        :param P: position for which I want the label
        :return:
        """
        node = self._validate(P)
        if node == self._root:
            return "Root has no label"
        return self._get_label_index_to_string(node._identifier, node._start, node._stop, len(node._children) == 0)

    def pathString(self, P):
        """
        The public method returns the substring associated to the path in T from the root to
        the node to which position P refers
        :param P: position for which I want the path string
        :return:
        """
        node = self._validate(P)
        path = ""
        while node is not self._root:
            path = self.getNodeLabel(self._make_position(node)) + path
            if node._parent is self._root:
                break
            else:
                node = node._parent

        if path[-1] == '$':
            return path[:-1]
        else:
            return path

    def getNodeDepth(self, P):
        """
        This public method returns the length of substring associated to the path in T
        from the root to the node to which position P refers
        :param P: position for which I want the depth
        :return:
        """
        node = self._validate(P)
        return node._depth

    def getNodeMark(self, P):
        """
        This public method returns the mark of the node u of T to which position P refers
        :param P: position for which I want the marker
        :return:
        """
        node = self._validate(P)
        return node._markers


    def child(self, P, s):
        """
        This public method returns the position of the child u of the node of T to which position P
        refers such that:
        -either s is a prefix of the substring labeling u,
        -or the substring labeling u is a prefix of s,
        if it exists, and it returns None otherwise
        :param P: position for which I want the child with the specific string
        :param s: string that must be compared
        :return:
        """
        node = self._validate(P)
        if s[0] in node._children:
            node = node._children.get(s[0]) #mi sposto nel figlio
            node_label = self.getNodeLabel(self._make_position(node))

            if node_label.endswith("$"):
                node_label = node_label[:-1]

            i = 0
            while i < len(node_label) and i < len(s):
                if node_label[i] != s[i]:
                    return None
                i += 1
            return self._make_position(node)
        else:
            return None



