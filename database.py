# Author:   Jon-Paul Boyd
# Date:     16/01/2018
# IMAT5118 A.I. Programming - Assignment 2
#
import mysql.connector
import logging
import coloured_text as ct
from constants import Constants


class Database:
    """Represent the database"""
    def __init__(self):
        self.user = 'imat5118'
        self.password = 'imat5118password'
        self.host = '127.0.0.1'
        self.database = 'sakila'
        self.connection = mysql.connector.connect(
            user=self.user,
            password=self.password,
            host=self.host,
            database=self.database)
        self.cursor = self.connection.cursor()
        logging.info("Database initialised")

    def execute_query(self, sqlquery):
        """Execute SQL query"""
        logging.info("Executing query: {}".format(sqlquery))
        self.cursor.execute(sqlquery)

    def output_results(self, cursor):
        row_idx = 0
        constants = Constants()

        for row in cursor:
            row_idx += 1
            col_idx = 0
            for column in row:
                if col_idx % 2 == 0:  # Column values in alternating colours to aid readability in shell
                    print(ct.Fore.YELLOW, end='')
                    print(column, end='')
                    print(" " + ct.Formatting.RESET_ALL, end='')
                else:
                    print(ct.Fore.WHITE, end='')
                    print(column, end='')
                    print(" " + ct.Formatting.RESET_ALL, end='')
                col_idx += 1

            print("")  # newline as end of row reached

        if row_idx == 0:
            print(ct.Fore.MAGENTA + ct.Formatting.BOLD + constants.nothing_found + ct.Formatting.RESET_ALL)

    def cursor_close(self):
        self.cursor.close()

    def connection_close(self):
        self.connection.close()
        logging.info("Database connection closed")
