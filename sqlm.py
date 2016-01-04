"""
This module provides MySQL functions.
"""

import mysql.connector


class Manager(object):
    def __init__(self, user, password, database=None, host='127.0.0.1'):
        self.cnx = mysql.connector.connect(user=user, password=password, database=database, host=host)
        self.cursor = self.cnx.cursor()

    def exe(self, query, display=0):
        # Just a shortcut for execution
        self.cursor.execute(query)
        if display:
            for this in self.cursor:
                print this

    def tablemaker(self, tablename, database):
        self.exe('use ' + database + ';')
        self.exe('')
