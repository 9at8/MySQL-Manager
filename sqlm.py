import sys
from time import sleep

try:
    import mysql.connector as cn
    print 'MySQL connection successful!'
except ImportError, e:
    print 'Import failed:', e.message
    print 'Trying to import \'MySQLdb\''
    sleep(2)
    try:
        import MySQLdb as cn
        print 'MySQL connection successful!'
    except ImportError, f:
        print 'Import failed:', f.message
        print 'Aborting.'
        for i in range(5, 0, -1):
            print i
            sleep(1)
        sys.exit()
