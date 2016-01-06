"""
This module provides MySQL functions.
"""

import mysql.connector


class Manager(object):
    def __init__(self, user, password, database, host='127.0.0.1'):
        self.database = database
        self.cnx = mysql.connector.connect(user=user, password=password,
                                           database=self.database, host=host)
        self.cursor = self.cnx.cursor(buffered=True)

    def exe(self, query, display=0):
        # Execution of a query
        # query = <query goes here>
        # display = <0 or 1> if you want to display the result
        self.cursor.execute(query)
        # self.cnx.commit()
        if display:
            for this in self.cursor:
                print this

    def table_create(self, table_name, number_of_columns):
        def checker(question, default_bool=0):
            p = question + ' ? (y/n):'
            q = raw_input(p).upper()
            if q == 'Y':
                if not default_bool:
                    return True
                else:
                    return True, raw_input('Enter default value: ')
            elif q == 'N':
                if not default_bool:
                    return False
                else:
                    return False, ''
            else:
                checker(question)

        tq = 'create table ' + table_name + ' ( '
        for i in range(number_of_columns):
            column_name = raw_input('Column ' + str(i + 1) + ' name: ')
            column_type = raw_input('Column ' + str(i + 1) + ' type: ')
            primary_key = 'Primary Key' if checker('Primary Key') else ''
            not_null = 'Not Null' if checker('Not Null') == True else ''
            default_check, default_value = checker('Default', 1)
            if (column_type.upper() not in ['INT', 'INTERGER']) and default_check:
                default_value = '"' + default_value + '"'
            default = 'Default ' + default_value if default_check else ''
            if (i + 1) == number_of_columns:
                tq += column_name + ' ' + column_type + ' ' + primary_key + \
                      ' ' + not_null + ' ' + default + ');'
            else:
                tq += column_name + ' ' + column_type + ' ' + primary_key + \
                      ' ' + not_null + ' ' + default + ', '
        self.exe(tq)
        self.cnx.commit()

    def table_insert(self, table):
        def more():
            _more = raw_input('Insert more values? (y/n): ').upper()
            if _more == 'Y':
                return False
            elif _more == 'N':
                return True
            else:
                more()

        self.exe('desc ' + table + ';')
        data = []
        for this in self.cursor:
            data.append(this)
        no_of_columns = len(data)
        while True:
            tq = 'insert into ' + table + ' values ('
            for i in range(no_of_columns):
                column_name = data[i][0]
                column_type = data[i][1]
                column_type_str = False if column_type.find('int') == 0 \
                    else True
                column_value = raw_input('Enter value of type ' +
                                         column_type + ' for column ' +
                                         column_name + ': ')
                if column_type_str:
                    column_value = '"' + column_value + '"'
                if (i + 1) == no_of_columns:
                    tq += column_value + ');'
                else:
                    tq += column_value + ', '
            self.exe(tq)
            self.cnx.commit()
            if more():
                break
