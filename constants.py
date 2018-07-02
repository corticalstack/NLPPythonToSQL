class Constants:
    """Represent constants"""
    def __init__(self):
        self.limit = 'LIMIT'
        self.search_tips_001 = 'Please enclose names within double quotes, e.g. "army flintstones" or "mae hoffman"'
        self.search_tips_002 = 'Use about to search movie descriptions, separating multiple keywords with and/or'
        self.prompt = 'How can I help? '
        self.quit = 'quit'
        self.goodbye = 'Goodbye'
        self.dont_understand = "Sorry I don't understand"
        self.nothing_found = "Nothing found matching your search criteria"
        self.fileroot = 'file:'
        self.path_grammar_rules = 'grammars\\'
        self.file_grammar_rules = 'grammars.csv'
        self.path_stopwords = 'stopwords\\'
        self.file_stopwords = 'stopwords.csv'
        self.path_synonyms = 'synonyms\\'
        self.file_synonym_set = 'synonym_generated_set.csv'
        self.failcode = '##fail##'
        self.double_quotes = '"'
        self.single_quote = "'"
        self.two_single_quotes = "''"
        self.leading_quotes = '``'
        self.percent = '%'

        self.syntactic_category_n = 'N'
        self.syntactic_category_v = 'V'
        self.syntactic_category_jj = 'JJ'
        self.syntactic_category_nns = 'NNS'

