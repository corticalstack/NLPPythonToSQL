# Author:   Jon-Paul Boyd
# Date:     16/01/2018
# IMAT5118 A.I. Programming - Assignment 2
#


class Word:
    """Represent the word"""
    def __init__(self, syntactic_category, wordnet_ss_type, word, grammar_ref):
        self.syntactic_category = syntactic_category
        self.wordnet_ss_type = wordnet_ss_type
        self.word = word
        self.grammar_ref = grammar_ref

    def __hash__(self):
        return hash((self.syntactic_category, self.wordnet_ss_type, self.word, self.grammar_ref))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.syntactic_category == other.syntactic_category and \
               self.wordnet_ss_type == other.wordnet_ss_type and self.word == other.word and other.grammar_ref == \
               self.grammar_ref

    def __ne__(self, other):
        return not self.__eq__(other)

