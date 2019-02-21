import pymysql as sql
import sys
sys.path.append('../')
from helper.helper import LibMS

dbname = "LibMS"

# List all the tables and their attributes.
@LibMS
def query1(cursor):
    print("==============================================================================")
    cursor.execute("SHOW TABLES;")
    print("Tables:")
    print(cursor.fetchall())
    print()
    cursor.execute("SELECT * FROM information_schema.columns where table_schema = '{}';".format(dbname)) 

    for p in cursor:
        print(p)
    print("==============================================================================")


# Display the total inventory in the ‘LMS’. For example, number of users, #books, #authors, #periodicals.
@LibMS
def query2(cursor):
    print("==============================================================================")
    
    cursor.execute("SELECT COUNT(*) FROM User;")
    print("Number of Users: ", cursor.fetchone()[0])

    cursor.execute("SELECT COUNT(*) FROM Book;")
    print("Number of Books: ", cursor.fetchone()[0])

    cursor.execute("SELECT COUNT(*) FROM Tag;")
    print("Number of Tags: ", cursor.fetchone()[0])

    cursor.execute("SELECT COUNT(*) FROM Author;")
    print("Number of Authors: ", cursor.fetchone()[0])

    cursor.execute("SELECT COUNT(*) FROM Periodical;")
    print("Number of Periodicals: ", cursor.fetchone()[0])

    cursor.execute("SELECT COUNT(*) FROM Paper;")
    print("Number of Papers: ", cursor.fetchone()[0])

    cursor.execute("SELECT COUNT(*) FROM Publisher;")
    print("Number of Publishers: ", cursor.fetchone()[0])

    cursor.execute("SELECT COUNT(*) FROM Message;")
    print("Number of Messages: ", cursor.fetchone()[0])

    print("==============================================================================")


# List the number of available books requested by a user.
@LibMS
def query3():
    pass


# List the author(s) of a given (queried) book.
@LibMS
def query4(cursor, book):
    print("==============================================================================")

    cursor.execute("SELECT * FROM Book WHERE Book.title='{}'".format(book))
    print(cursor.fetchone())

    print("==============================================================================")
    

if __name__ == "__main__":
    query2()