import pymysql as sql
import sys
sys.path.append('../')
from helper.helper import LibMS

dbname = "LibMS"

@LibMS
def query1(cursor):
    cursor.execute("SHOW TABLES;")
    print("Tables:")
    print(cursor.fetchall())
    print()
    cursor.execute("SELECT * FROM information_schema.columns where table_schema = '{}';".format(dbname)) 

    for p in cursor:
        print(p)


@LibMS
def query2(cursor):
        pass


@LibMS
def query3():
        pass

if __name__ == "__main__":
    query1()
