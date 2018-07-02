# Author:   Jon-Paul Boyd
# Date:     16/01/2018
# IMAT5118 A.I. Programming - Assignment 2
# Parse Natural Language (NL) queries into formal SQL for reading movie and actor info from MySQL database
import logging
import sys
import coloured_text as ct
from parse import Parse
import mysql.connector
from os import path
from constants import Constants
from database import Database
from grammar_config import Grammarconfig


def main():
    constants = Constants()
    database = Database()
    parse = Parse()
    grammar_config = Grammarconfig()
    user_command = ""
    query_suffix = ''
    if sys.argv[1][0:5] == constants.limit:
        query_suffix = ' ' + sys.argv[1]

    # First time search tips
    print(ct.Fore.MAGENTA + ct.Formatting.BOLD + constants.search_tips_001 + ct.Formatting.RESET_ALL)
    print(ct.Fore.MAGENTA + ct.Formatting.BOLD + constants.search_tips_002 + ct.Formatting.RESET_ALL)

    while user_command != constants.quit:
        print("")
        user_command = input(ct.Fore.MAGENTA + ct.Formatting.BOLD + constants.prompt + ct.Formatting.RESET_ALL)
        logging.info("User command: {}".format(user_command))
        if user_command != constants.quit:
            query = parse.nl_command(user_command, grammar_config)
            if query != constants.failcode:
                if constants.limit not in query:  # limit result set if set in runtime & not already restricted in query
                    query = query + query_suffix
                try:
                    database.execute_query(query)
                except mysql.connector.Error as err:
                    logging.info("SQL query syntax error: {}".format(err))
                else:
                    database.output_results(database.cursor)
            else:
                print(ct.Fore.RED + ct.Formatting.BOLD + constants.dont_understand + ct.Formatting.RESET_ALL)
                logging.info("Query parsing failed")
        else:
            break

    database.cursor_close()
    database.connection_close()
    print(ct.Fore.MAGENTA + ct.Formatting.BOLD + constants.goodbye + ct.Formatting.RESET_ALL)


if __name__ == '__main__':
    import logging.config
    log_file_path = path.join(path.dirname(path.abspath(__file__)), 'logging.conf')
    logging.config.fileConfig(log_file_path)
    logging.info("Runtime configuration: {}".format(sys.argv[1]))
    main()
