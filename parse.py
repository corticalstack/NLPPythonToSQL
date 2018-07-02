# Author:   Jon-Paul Boyd
# Date:     16/01/2018
# IMAT5118 A.I. Programming - Assignment 2
# This module transforms the natural language query to formal SQL query
#
import os
import logging
from nltk import load_parser
from nltk.tokenize import word_tokenize
from constants import Constants


class Parse:
    """Represent the parser"""
    def __init__(self):
        """Initialise parse"""
        self.feature_cfg = ""
        self.configuration_file = ""

        self.parser_sem_tag = 'SEM'

        self.sql_operator_and = ' AND '
        self.sql_operator_or = ' OR '
        self.sql_operator_like_tag = '#LIKE'
        self.sql_select_where_title = "SELECT * FROM film_list where title = '"
        self.predicate_mask_like_description = "description LIKE '%#LIKE%'"

        self.token_about = 'about'
        self.token_and = 'and'
        self.token_or = 'or'
        self.token_starring_tag = '#STARRING'

    @staticmethod
    def _generate_path_grammar_rules():
        constants = Constants()
        cwd = os.path.dirname(__file__)
        pathname = constants.fileroot + os.path.join(cwd, constants.path_grammar_rules)
        return pathname

    @staticmethod
    def to_lowercase(tokens):
        # convert to lowercase all NL query tokens except movie and person names (as per movie db data)
        constants = Constants()
        is_movie_or_actor_start = False
        is_movie_or_actor_end = False
        is_first_token_after_leading_quote = True
        query = ''
        for idx, token in enumerate(tokens):
            if token == constants.leading_quotes and (not is_movie_or_actor_start):
                is_movie_or_actor_start = True
                query = query + ' ' + token
                continue

            if token == constants.two_single_quotes:
                is_movie_or_actor_end = True
                query = query + token
                continue

            if is_movie_or_actor_start and (not is_movie_or_actor_end):
                if is_first_token_after_leading_quote:
                    is_first_token_after_leading_quote = False
                    query = query + token
                else:
                    query = query + ' ' + token

                continue

            token_lower = token.lower()
            tokens[idx] = token_lower
            query = query + ' ' + token_lower

        return tokens, query

    @staticmethod
    def build_nl_query_matching_synonyms(nl_query, grammar, grammar_config):
        # Attempt match of each NL query word against synonym words for current grammar rule, and replace with
        # words known to be right-hand side (rhs) terminals in the grammar rule
        query = nl_query
        token_list = nl_query.split()

        # for all tokens in nl query
        for token_val in token_list:
            synonyms_for_all_tokens_found = False
            for syn in grammar_config.synonyms:
                if syn.grammar_ref == grammar.ref:
                    if token_val == syn.synonym:
                        query = query.replace(token_val, syn.word, 1)
                        logging.info("Synonym match: {} -> {}".format(token_val, syn.word))
                        break
        if query != nl_query:
            return query  # at least one word replacement
        else:
            return False

    def nl_command(self, nl_query, grammar_config):
        """Parse Natural Language Command"""
        constants = Constants()

        tokens = word_tokenize(nl_query)
        logging.info("NL query tokens: {}".format(tokens))

        # compile SQL query for stand-alone movie title
        sql_query = self.movie_title(tokens)
        if sql_query:
            logging.info("SQL query: {}".format(sql_query))
            return sql_query

        # convert natural language query to lowercase (except names) for robust grammar rule matching
        tokens, nl_query = self.to_lowercase(tokens)
        logging.info("NL query after lower case: {}".format(nl_query))
        logging.info("NL query tokens after lower case: {}".format(tokens))

        # is NL query for starring actor?
        starring, nl_query = self.starring(tokens, nl_query)
        logging.info("Starring: {}".format(starring))

        # is NL query about with keywords?
        is_about, nl_query = self.about(tokens, nl_query)
        logging.info("About: {}".format(is_about))

        # Iterate grammar rule catalog
        for grammar in grammar_config.grammar_rules:
            if grammar.enabled == 'N':
                continue

            # add user-provided NL query to list after above pre-processing as primary query
            # any matching synonym based query will follow
            nl_queries = list()
            nl_queries.append(nl_query)

            logging.info("Parsing grammar file: {}".format(grammar.file))

            # load grammar rule into NLTK parser
            self.configuration_file = self._generate_path_grammar_rules() + grammar.file
            self.feature_cfg = load_parser(self.configuration_file, trace=0)  # trace=2 for debug

            # build NL query variation
            nl_query_variation = self.build_nl_query_matching_synonyms(nl_query, grammar, grammar_config)
            if nl_query_variation:
                nl_queries.append(nl_query_variation)

            query_count = 0
            for nlq in nl_queries:
                query_count += 1
                try:
                    trees = list(self.feature_cfg.parse(nlq.split()))  # parse NL query with current grammar rule
                except ValueError as ve:
                    logging.info("Grammar {} failed to parse NL query with : {}".format(grammar.file, ve))
                    continue  # current grammar rule cannot parse NL query
                else:
                    try:
                        logging.info("Parse trees: {}".format(trees))
                        if not trees:
                            continue

                        if query_count == 1:
                            logging.info("Grammar file resolves original NL query: {}".format(grammar.file))
                        else:
                            logging.info("Grammar file resolves synonym transformed NL query: {}".format(grammar.file))

                        top_tree_semantics = trees[0].label()[self.parser_sem_tag]  # get tree top entry semantic output
                        top_tree_semantics = [s for s in top_tree_semantics if s]  # first SEM entry tuple to list
                        logging.info("Top tree semantics: {}".format(top_tree_semantics))
                        sql_query = ' '.join(top_tree_semantics)  # join each top production element separated by space

                        # put "starring" or "about" predicate values into SQL query
                        if starring:
                            starring_val = constants.single_quote + constants.percent + starring \
                                        + constants.percent + constants.single_quote
                            sql_query = sql_query.replace(self.token_starring_tag, starring_val)
                        if is_about:
                            sql_query = sql_query + is_about

                        # we should now have a well-formed query
                        logging.info("SQL query: {}".format(sql_query))
                        return sql_query
                    except IndexError:
                        continue

        return constants.failcode

    def movie_title(self, tokens):
        # determine if NL query is only a movie title, and convert title to upper-case (add resilience, as per db data)
        constants = Constants()
        movie_title = ''
        is_movie_title_start = False
        is_movie_title_end = False

        for idx, token in enumerate(tokens):
            if idx == 0 and token == constants.leading_quotes:
                is_movie_title_start = True
                continue

            if token == constants.two_single_quotes:
                is_movie_title_end = True
                continue

            # Not a movie title as further tokens follow
            if is_movie_title_end:
                is_movie_title_end = False
                break

            if idx != 1:
                movie_title += ' '

            movie_title += token.upper()

        if is_movie_title_start and is_movie_title_end:
            sql_query = self.sql_select_where_title + movie_title + constants.single_quote
            return sql_query

    def starring(self, tokens, query):
        # determine if NL query includes person name and if so build name string for later re-injection into SQL query
        # convert name to upper-case (add resilience, as per db data)
        constants = Constants()
        starring = ''
        is_starring_leading_quotes = False

        for idx, token in enumerate(tokens):
            if token != constants.leading_quotes and (not is_starring_leading_quotes):
                continue

            if token == constants.leading_quotes:
                is_starring_leading_quotes = True
                query = query.replace(constants.leading_quotes, self.token_starring_tag, 1)
                continue

            if token == constants.two_single_quotes:
                query = query.replace(constants.two_single_quotes, '', 1)
                break

            if is_starring_leading_quotes:
                query = query.replace(token, '', 1)
                starring = starring + ' ' + token.upper()

        starring = starring.strip()
        return starring, query

    def about(self, tokens, query):
        # determine if NL query includes "about" keyword - signifies search criteria SQL WHERE-clause predicate values
        # on name and if so build name string for later re-injection into SQL query
        # convert name to upper-case (add resilience, as per db data)
        is_about = False
        is_about_mask = self.predicate_mask_like_description
        is_about_string = ''

        for idx, token in enumerate(tokens):
            if token == self.token_about:
                is_about = True

                # query will be parsed through fcfg grammar
                # keywords to right of 'about' will be added to predicate clause
                about_index = query.index(self.token_about) + len(self.token_about)
                query = query[0:about_index] # left-side query up to and including "about" keyword
                continue

            if not is_about:
                continue

            if token == self.token_and:  # add WHERE clause values with AND
                is_about_string = is_about_string + self.sql_operator_and
                continue

            if token == self.token_or:  # add WHERE clause values with OR
                is_about_string = is_about_string + self.sql_operator_or
                continue

            predicate_string = is_about_mask
            predicate_string = predicate_string.replace(self.sql_operator_like_tag, token)
            is_about_string = is_about_string + predicate_string

        return is_about_string, query
