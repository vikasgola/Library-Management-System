import pandas as pd
from Library_Management_System.helper.helper import *

# List all the tables and their attributes.
@LibMS
def query1(cursor):
    print("==================================Query 1============================================")
    cursor.execute("SHOW TABLES;")
    print("Tables:")
    print(cursor.fetchall())
    print()
    cursor.execute("SELECT * FROM information_schema.columns where table_schema = '{}';".format(dbname)) 

    print(pd.DataFrame(list(cursor.fetchall())))

    print("==============================================================================")


# Display the total inventory in the ‘LMS’. For example, number of users, #books, #authors, #periodicals.
@LibMS
def query2(cursor):
    print("==================================Query 2============================================")
    
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

    cursor.execute("SELECT COUNT(*) FROM BookHistory;")
    print("Number of BookHistory: ", cursor.fetchone()[0])

    cursor.execute("SELECT COUNT(*) FROM PeriodicalHistory;")
    print("Number of periodicalHistory: ", cursor.fetchone()[0])

    print("==============================================================================")


# List the number of available books requested by a user.
@LibMS
def query3(cursor, requested_id_list):
    print("==================================Query 3============================================")

    q = ""
    for i in range(len(requested_id_list)):
        q += "( Book.book_id = "+str(requested_id_list[i])+" AND Book.user_id IS NULL ) OR"
    q = q[:-2]

    cursor.execute("""
                SELECT COUNT(*) FROM Book WHERE  {}""".format(q))
    print("Number of Available Books request by user are: ", cursor.fetchall()[0][0])

    print("==============================================================================")


# List the author(s) of a given (queried) book.
@LibMS
def query4(cursor, bookid):
    print("==================================Query 4============================================")

    cursor.execute("""
                SELECT Author.name FROM Author, Book, BookAuthor WHERE Author.author_id = BookAuthor.author_id AND BookAuthor.book_id = {};""".format(str(bookid)))
    print("Authors of Book with id, "+str(bookid)+", are", cursor.fetchall()[0])

    print("==============================================================================")

# List the total number of books issued for a user.
@LibMS
def query5(cursor, userid):
    print("==================================Query 5============================================")

    cursor.execute("""SELECT COUNT(*) FROM Book WHERE Book.user_id = {}""".format(str(userid)))
    numberofissued = cursor.fetchall()[0][0]
    print("Total Number of Books Issued for User with userid "+str(userid)+ " is" , numberofissued)

    print("==============================================================================")
    return numberofissued
    
# Check whether a user is allowed to borrow a book or not.
@LibMS
def query6(cursor, userid):
    print("==================================Query 6============================================")

    count = query5(userid=userid)
    cursor.execute("SELECT maxbooks FROM Capacity, User WHERE Capacity.usertype = User.usertype AND User.user_id = {}".format(str(userid)))
    if(count >= cursor.fetchall()[0][0]):
        print("User is not allowed to Boorow Book.")
    else:
        print("User is allowed to Boorow Book.")
    print("==============================================================================")


# List the number of issued and returned books on daily basis (for a given day/period).
@LibMS
def query7(cursor, date1, date2):
    print("==================================Query 7============================================")

    cursor.execute("SELECT COUNT(*) FROM BookHistory WHERE BookHistory.issuedate > '{}' AND BookHistory.issuedate < '{}';".format(date1, date2))
    print("Number of issued booked from "+date1+" to "+ date2+": ", cursor.fetchall()[0][0])

    cursor.execute("SELECT COUNT(*) FROM BookHistory WHERE BookHistory.returndate > '{}' AND BookHistory.returndate < '{}';".format(date1, date2))
    print("Number of returned booked from "+date1+" to "+ date2+": ", cursor.fetchall()[0][0])

    print("==============================================================================")


# List the users with book details if there are any dues.
@LibMS
def query8(cursor):
    print("==================================Query 8============================================")
    print("These are the users which have dues with these books")

    cursor.execute("SELECT Book.*, User.* FROM Book, User, Capacity WHERE Book.user_id = User.user_id AND (SELECT DATEDIFF(NOW(), Book.issuetime) AS days) > Capacity.maxdays AND Capacity.usertype = User.usertype;")
    print(pd.DataFrame(list(cursor.fetchall())))

    print("==============================================================================")


# List the newly added book records for a given period.
@LibMS
def query9(cursor, date1, date2):
    print("==================================Query 9============================================")

    cursor.execute("SELECT * FROM Book WHERE Book.adddate between '{}' and '{}';".format(date1, date2))
    out = pd.DataFrame(list(cursor.fetchall()))
    print(out)

    print("==============================================================================")

# Display the user name and the books issued to them.
@LibMS
def query10(cursor):
    print("==================================Query 10============================================")

    cursor.execute("SELECT User.name, Book.title FROM User, Book WHERE Book.user_id = User.user_id;")
    out = pd.DataFrame(list(cursor.fetchall()), columns=["User Name", "Book Title"])
    print(out)

    print("==============================================================================")

# Display all the books with all details issued to a user.
@LibMS
def query11(cursor, userid):
    print("==================================Query 11============================================")

    cursor.execute("SELECT * FROM Book WHERE Book.user_id = {};".format(userid))
    out = pd.DataFrame(list(cursor.fetchall()))
    print(out)

    print("==============================================================================")


@LibMS
def question6ForAUser(cursor, userid, printzero=True):
    if printzero:
        print("==================================Question 6 For a User============================================")
    fine = 0
    try:
        cursor.execute("""SELECT DATEDIFF(NOW(), (SELECT Book.issuetime FROM Book, User, Capacity WHERE Book.user_id = User.user_id AND Book.user_id = {} 
                    AND (SELECT DATEDIFF(NOW(), Book.issuetime) AS days) > Capacity.maxdays 
                    AND Capacity.usertype = User.usertype)) AS days ;""".format(str(userid)))
        fine = cursor.fetchall()[0][0]
        if fine != None:
            print("Fine for user with userid ",userid, "is ", fine)
        else:
            raise Exception("Null Fine")
    except:
        if printzero: 
            print("Fine for user with userid ",userid, "is 0")
    if printzero:
        print("==============================================================================")
    return fine
    

@LibMS
def question6ForAllUser(cursor):
    print("==================================Question 6 For all User============================================")

    cursor.execute("SELECT COUNT(*) FROM User;")
    for i in range(int(cursor.fetchone()[0])):
        question6ForAUser(userid=i+1, printzero=False)
    print("==============================================================================")

 

def runQueries():
    query1()
    query2()
    query3(requested_id_list=["1","2"])
    query4(bookid=1)
    query5(userid=1)
    query6(userid=1)
    query8()
    query7(date1="2017-06-06", date2="2018-01-01")
    query9(date1="2018-01-01", date2="2018-06-01")
    query10()
    query11(userid=1)

    question6ForAUser(userid=1)
    question6ForAllUser()


if __name__ == "__main__":
    setUsername("lmsuser")
    setPassword("lmsuserpassword")
    runQueries()