import pandas as pd
from Library_Management_System.helper.helper import *

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

    cursor.execute("SELECT COUNT(*) FROM History;")
    print("Number of History: ", cursor.fetchone()[0])

    print("==============================================================================")


# List the number of available books requested by a user.
# TODO: not completed
@LibMS
def query3(cursor):
    print("==============================================================================")

    cursor.execute("""
                SELECT COUNT(*) FROM Book WHERE Book.user_id IS NULL""")
    print("Number of Available Books request by user are: ", cursor.fetchall()[0][0])

    print("==============================================================================")


# List the author(s) of a given (queried) book.
@LibMS
def query4(cursor, book):
    print("==============================================================================")

    cursor.execute("""
                SELECT Author.name FROM Author WHERE author_id = (SELECT BookAuthor.author_id FROM BookAuthor Where BookAuthor.book_id = (SELECT Book.book_id FROM Book WHERE Book.title='{}' LIMIT 1 ) )""".format(book))
    print("Authors of Book, "+book+", are", cursor.fetchall()[0])

    print("==============================================================================")

# List the total number of books issued for a user.
@LibMS
def query5(cursor, user):
    print("==============================================================================")

    cursor.execute("""SELECT COUNT(*) FROM Book WHERE Book.user_id = (SELECT User.user_id FROM User WHERE User.name='{}' LIMIT 1) LIMIT 1""".format(user))
    print("Total Number of Books Issued for "+user+ " is" , cursor.fetchall()[0][0])

    print("==============================================================================")

# Check whether a user is allowed to borrow a book or not.
@LibMS
def query6(cursor):
    pass


# List the number of issued and returned books on daily basis (for a given day/period).
@LibMS
def query7(cursor, date1, date2):
    print("==============================================================================")

    cursor.execute("SELECT COUNT(*) FROM History WHERE History.issuedate > '{}' AND History.issuedate < '{}';".format(date1, date2))
    print("Number of issued booked on "+date1+" to "+ date2+": ", cursor.fetchall()[0][0])

    cursor.execute("SELECT COUNT(*) FROM History WHERE History.returndate > '{}' AND History.returndate < '{}';".format(date1, date2))
    print("Number of returned booked on "+date1+" to "+ date2+": ", cursor.fetchall()[0][0])

    print("==============================================================================")


# List the users with book details if there are any dues.
@LibMS
def query8(cursor):
    pass

# List the newly added book records for a given period.
@LibMS
def query9(cursor, date1, date2):
    print("==============================================================================")

    cursor.execute("SELECT * FROM Book WHERE Book.adddate between '{}' and '{}';".format(date1, date2))
    out = pd.DataFrame(list(cursor.fetchall()))
    print(out)

    print("==============================================================================")

# Display the user name and the books issued to them.
@LibMS
def query10(cursor):
    print("==============================================================================")

    cursor.execute("SELECT User.name, Book.title FROM User, Book WHERE Book.user_id = User.user_id;")
    out = pd.DataFrame(list(cursor.fetchall()))
    print(out)

    print("==============================================================================")

# Display all the books with all details issued to a user.
@LibMS
def query11(cursor):
    print("==============================================================================")

    cursor.execute("SELECT * FROM Book WHERE Book.user_id IS NOT NULL;")
    out = pd.DataFrame(list(cursor.fetchall()))
    print(out)

    print("==============================================================================")


def runQueries():
    query1()
    query2()
    query3()
    query4(book="Let them eat cake.")
    query5(user="Shad Becker")
    query7(date1="2017-06-06", date2="2018-01-01")
    query9(date1="2018-01-01", date2="2018-06-01")
    query10()
    query11()