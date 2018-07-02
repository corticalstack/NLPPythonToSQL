# Author:   Jon-Paul Boyd
# Date:     16/01/2018
# IMAT5118 A.I. Programming - Assignment 2
# This module:
#   loads the grammar rules
#   builds a synonym set from the terminal right hand side nouns/verbs in the rules
#
import logging
import os
import csv
from constants import Constants
from nltk import load_parser
from nltk.corpus import wordnet
from grammar import Grammar
from stopword import Stopword
from word import Word
from synonym import Synonym


class Grammarconfig:
    """Represent the grammar config"""
    def __init__(self):
        self.grammar_rules = list()
        self.stopwords = list()
        self.words = set()
        self.synonyms = list()
        self.load_grammar_rules()
        self.load_stopwords()
        self.build_synonyms()

    @staticmethod
    def _generate_path():
        constants = Constants()
        cwd = os.path.dirname(__file__)
        pathname = constants.fileroot + os.path.join(cwd, constants.path_grammar_rules)
        return pathname

    def load_grammar_rules(self):
        constants = Constants()
        with open(constants.path_grammar_rules + constants.file_grammar_rules) as csvfile:
            readcsv = csv.reader(csvfile, delimiter=',')
            for row in readcsv:
                ref = row[0]
                file = row[1]
                category = row[2]
                enabled = row[3]
                grammar = Grammar(ref, file, category, enabled)
                self.grammar_rules.append(grammar)

    def load_stopwords(self):
        constants = Constants()
        with open(constants.path_stopwords + constants.file_stopwords) as csvfile:
            readcsv = csv.reader(csvfile, delimiter=',')
            for row in readcsv:
                stopword = row[0]
                enabled = row[1]
                stopword = Stopword(stopword, enabled)
                self.stopwords.append(stopword)

    def build_synonyms(self):
        constants = Constants()
        logging.info("Building synonyms started")
        for grammar in self.grammar_rules:
            if grammar.enabled == 'N':
                continue

            # load rule into parser so rhs terminal words can be extracted from lhs noun/verbs
            configuration_file = self._generate_path() + grammar.file
            feature_cfg = load_parser(configuration_file, trace=0)
            productions = feature_cfg.grammar().productions()
            for prod in productions:
                prod_str = str(prod)
                prod_lhs_rhs = prod_str.split('-> ')
                rhs_terminal = prod_lhs_rhs[1].replace(constants.single_quote, "")
                if not rhs_terminal.isalpha():
                    continue

                # ignore configured stopwords e.g. pg, r
                is_stopword = False
                for stopword in self.stopwords:
                    if rhs_terminal == stopword.stopword:
                        is_stopword = True

                if is_stopword:
                    continue

                syntactic_category = ''
                wordnet_synset_type = ''

                if prod_str[0:2] == constants.syntactic_category_jj:
                    syntactic_category = constants.syntactic_category_jj
                    wordnet_synset_type = 's'
                elif prod_str[0:1] == constants.syntactic_category_n:
                    syntactic_category = constants.syntactic_category_n
                    wordnet_synset_type = 'n'
                elif prod_str[0:1] == constants.syntactic_category_v:
                    syntactic_category = constants.syntactic_category_v
                    wordnet_synset_type = 'n'
                elif prod_str[0:3] == constants.syntactic_category_nns:
                    syntactic_category = constants.syntactic_category_nns
                    wordnet_synset_type = 'n'

                # compile list of words from rules
                if syntactic_category != '':
                    self.words.add(Word(syntactic_category, wordnet_synset_type, rhs_terminal, grammar.ref))

        # compile synonym set from extracted word list
        for w in self.words:
            for syn in wordnet.synsets(w.word):
                for lemma in syn.lemmas():
                    if lemma.name() != w.word:
                        synonym = Synonym(w.syntactic_category, w.word, lemma.name().lower(), w.grammar_ref)
                        self.synonyms.append(synonym)

        logging.info("Building synonyms completed")

        try:
            file = open(constants.path_synonyms + constants.file_synonym_set, "w")
            file.write('grammar_ref' + ',' + 'syntactic_category' + ',' + 'rule word' + ',' + 'synonym' + '\n')
            for syn in self.synonyms:
                fileline = syn.grammar_ref + ',' + syn.syntactic_category + ',' + syn.word + ',' + \
                           syn.synonym + '\n'
                file.write(fileline)
            file.close()
        except EnvironmentError as err:
            logging.warning("Failed to write synonym set: {}".format(err))
