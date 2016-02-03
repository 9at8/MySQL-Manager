"""
This module provides MySQL functions.
"""

import mysql.connector
from time import localtime


class Manager(object):
    file_log = open('mysql.log', 'a')

    # This is the log file where all the MySQL commands executed will be
    # stored along with their time of execution.

    def __init__(self, user, password, database, host='127.0.0.1'):
        self.database = database
        self.cnx = mysql.connector.connect(user=user, password=password,
                                           database=self.database, host=host)
        # Localhost is selected if no host is provided.

        self.cursor = self.cnx.cursor(buffered=True)
        # For unbuffered cursors, rows are not fetched from the server until
        # a row-fetching method is called. In this case, we must be sure to
        # fetch all rows of the result set before executing any other
        # statements on the same connection, or an
        # InternalError (Unread result found) exception will be raised.

        # Buffered cursors can be useful in situations where multiple queries,
        # with small result sets, need to be combined or computed with each
        # other.

    @staticmethod
    def __log(query):
        # Stores all the MySQL commands executed by exe function in a file
        # along with the time of execution.
        time_now = str(localtime().tm_hour) + ':' + str(localtime().tm_min) + \
                   ' - ' + str(localtime().tm_mday) + '/' + \
                   str(localtime().tm_mon) + '/' + str(localtime().tm_year) + \
                   ' -> '
        Manager.file_log.write(time_now + query + '\n')
        Manager.file_log.flush()
        # Flushing changes to file.

    def exe(self, query, display=0):
        # Execution of a query plus logging of commands
        # query = <query goes here>
        # display = <0 or 1> if you want to display the result
        Manager.__log(query)
        self.cursor.execute(query)
        if display:
            row = self.cursor.fetchone()
            while row:
                print row
                row = self.cursor.fetchone()

    @staticmethod
    def __checker(question, default_bool=0):
        # This provides interface for yes/no questions by returning
        # True or False
        # It can also be used to set the value for default parameter
        # in MySQL
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
            Manager.__checker(question)

    def table_create(self, table_name, number_of_columns):
        # Creates a table.

        tq = 'create table ' + table_name + ' ( '
        # tq is the main query
        for i in range(number_of_columns):
            # This loop generates the query 'tq'

            column_name = raw_input('Column ' + str(i + 1) + ' name: ')
            column_type = raw_input('Column ' + str(i + 1) + ' type: ')

            # Conditional Assignment with the help of __checker function.
            primary_key = 'Primary Key' if Manager.__checker('Primary Key') else ''
            not_null = 'Not Null' if Manager.__checker('Not Null') else ''
            default_check, default_value = Manager.__checker('Default', 1)

            if (column_type.upper() not in ['INT', 'INTERGER']) and default_check:
                default_value = '"' + default_value + '"'
                # Adds strings to default value if it is not an integer

            # Conditional Assignment.
            default = 'Default ' + default_value if default_check else ''

            # Adds ');' at the end in the last query and adds ', ' otherwise.
            if (i + 1) == number_of_columns:

                tq += column_name + ' ' + column_type + ' ' + primary_key + \
                      ' ' + not_null + ' ' + default + ');'
            else:
                tq += column_name + ' ' + column_type + ' ' + primary_key + \
                      ' ' + not_null + ' ' + default + ', '

        self.exe(tq)

        # self.cnx.commit() is necessary to commit changes to database.
        self.cnx.commit()

    def table_insert(self, table):
        # Inserts values into existing table.

        def more():
            # Just used for checking if the user wants to insert more values.

            _more = raw_input('Insert more values? (y/n): ').upper()
            if _more == 'Y':
                return True
            elif _more == 'N':
                return False
            else:
                more()

        # Used to find out the number of columns in the table to avoid
        # overflow or underflow
        self.cursor.execute('desc ' + table + ';')
        data = []
        for this in self.cursor:
            data.append(this)
        no_of_columns = len(data)

        while True:
            tq = 'insert into ' + table + ' values ('
            for i in range(no_of_columns):
                # This loop generates the query 'tq'

                column_name = data[i][0]
                column_type = data[i][1]
                column_type_str = False if column_type.find('int') == 0 \
                    else True
                column_value = raw_input('Enter value of type ' +
                                         column_type + ' for column ' +
                                         column_name + ': ')

                if column_type_str:
                    column_value = '"' + column_value + '"'

                # Adds ');' at the end in the last query and adds ', ' otherwise.
                if (i + 1) == no_of_columns:
                    tq += column_value + ');'
                else:
                    tq += column_value + ', '

            self.exe(tq)

            # self.cnx.commit() is necessary to commit changes to database.
            self.cnx.commit()

            if not more():
                break

    def table_alter(self, table):
        # Alters the specified table.

        more = raw_input('Alter table \'' + table + '\'? (y/n): ')
        while True:
            try:
                if more.lower() == 'n':
                    break
                elif more.lower() == 'y':
                    pass
                else:
                    print 'Enter a valid choice.'
                    self.table_alter(table)
            except AttributeError:
                print 'Enter a string.'
                self.table_alter(table)

            # Choices go here.
            c = '''What do you want to do?
                    1. Add column
                    2. Modify column
                    3. Drop column\n'''

            # Number of choices.
            _numc = 3

            while True:
                # Forces user to choose from a specific set of values.

                try:
                    choice = int(raw_input(c))
                    if not (0 < choice <= _numc):
                        print 'Enter a valid number.'
                        continue
                    break
                except ValueError:
                    print 'Enter an integer.'

            # Initial query is generated.
            query = 'alter table ' + table

            if choice == 1:
                # Generates query for adding a column.

                column_name = raw_input('Enter column name to be added: ')
                column_type = raw_input('Enter column type: ')

                # Conditional Assignment with the help of __checker function.
                not_null = 'Not Null' if Manager.__checker('Not Null') else ''
                default_check, default_value = Manager.__checker('Default', 1)

                if (column_type.upper() not in ['INT', 'INTERGER']) and default_check:
                    default_value = '"' + default_value + '"'

                # Conditional Assignment.
                default = 'Default ' + default_value if default_check else ''

                query += ' add ' + column_name + ' ' + column_type + ' ' \
                         + not_null + ' ' + default + ';'
                self.exe(query)

                # self.cnx.commit() is necessary to commit changes to database.
                self.cnx.commit()

            elif choice == 2:
                # Generates query for modifying a column.

                column_name = raw_input('Enter column name to be modified: ')
                column_type = raw_input('Enter column type: ')

                # Conditional Assignment with the help of __checker function.
                not_null = 'Not Null' if Manager.__checker('Not Null') else ''
                default_check, default_value = Manager.__checker('Default', 1)

                if (column_type.upper() not in ['INT', 'INTERGER']) and default_check:
                    default_value = '"' + default_value + '"'

                # Conditional Assignment.
                default = 'Default ' + default_value if default_check else ''
                query += ' modify ' + column_name + ' ' + column_type + ' ' \
                         + not_null + ' ' + default + ';'
                self.exe(query)

                # self.cnx.commit() is necessary to commit changes to database.
                self.cnx.commit()
            elif choice == 3:
                # Generates query for for dropping a column.

                column_name = raw_input('Enter column name to be dropped: ')
                query += ' drop column ' + column_name + ';'
                self.exe(query)

                # self.cnx.commit() is necessary to commit changes to database.
                self.cnx.commit()

            more = raw_input('Alter table \'' + table + '\' more? (y/n): ')

    def table_drop(self, table):
        # Clears data + structure

        query = 'drop table ' + table + ';'
        self.exe(query)

        # self.cnx.commit() is necessary to commit changes to database.
        self.cnx.commit()

    def table_delete(self, table):
        # Clears only data

        query = 'delete from ' + table + ';'
        self.exe(query)

        # self.cnx.commit() is necessary to commit changes to database.
        self.cnx.commit()
