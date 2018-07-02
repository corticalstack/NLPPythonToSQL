# Author:   Jon-Paul Boyd
# Date:     16/01/2018
# IMAT5118 A.I. Programming - Assignment 2
#


class Synonym:
    """Represent the synonym"""
    def __init__(self, syntactic_category, word, synonym, grammar_ref):
        self.syntactic_category = syntactic_category
        self.word = word
        self.synonym = synonym
        self.grammar_ref = grammar_ref

