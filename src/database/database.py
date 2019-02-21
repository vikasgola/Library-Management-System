import sys
sys.path.append('../')
from helper.helper import LibMS

@LibMS
def createDatabase():
    connection = sql.connect(host='localhost', user='lms', password="openlibrary")
    
    try:
        with connection.cursor() as cursor:
            cursor.execute("CREATE DATABASE LibMS;")
        connection.commit()
    finally:
        connection.close()


def createTables(cursor):
        cursor.execute("""CREATE TABLE User(
                            user_id INT NOT NULL AUTO_INCREMENT,
                            name VARCHAR(40) NOT NULL,
                            username VARCHAR(40) NOT NULL,
                            password VARCHAR(256) NOT NULL,
                            email VARCHAR(50) NOT NULL,
                            publisher_id INT NOT NULL,
                            PRIMARY KEY ( user_id ) );""")
        
        cursor.execute("""CREATE TABLE Book(
                            book_id INT NOT NULL AUTO_INCREMENT,
                            pages INT NOT NULL,
                            title VARCHAR(40) NOT NULL,
                            year YEAR(4) NOT NULL,
                            isbn VARCHAR(13) NOT NULL,
                            addtime DATE NOT NULL,
                            issuetime DATETIME NOT NULL,
                            PRIMARY KEY ( book_id ) );""")

        cursor.execute("""CREATE TABLE Message(
                            message_id INT NOT NULL AUTO_INCREMENT,
                            text VARCHAR(1000) NOT NULL,
                            user_id INT NOT NULL,
                            PRIMARY KEY ( message_id ) );""")

        cursor.execute("""CREATE TABLE Periodical(
                            periodical_id INT NOT NULL AUTO_INCREMENT,
                            title VARCHAR(40) NOT NULL,
                            year YEAR(4) NOT NULL,
                            isbn VARCHAR(13) NOT NULL,
                            volume INT NOT NULL,
                            user_id INT NOT NULL,
                            publisher_id INT NOT NULL, 
                            PRIMARY KEY ( periodical_id ) );""")


        cursor.execute("""CREATE TABLE Publisher(
                            publisher_id INT NOT NULL AUTO_INCREMENT,
                            name VARCHAR(40) NOT NULL,
                            PRIMARY KEY ( publisher_id ) );""")
        
        cursor.execute("""CREATE TABLE Tag(
                            tag_id INT NOT NULL AUTO_INCREMENT,
                            value VARCHAR(40) NOT NULL,
                            PRIMARY KEY ( tag_id ) );""")
        
        cursor.execute("""CREATE TABLE Paper(
                            paper_id INT NOT NULL AUTO_INCREMENT,
                            name VARCHAR(40) NOT NULL,
                            periodical_id INT NOT NULL,
                            PRIMARY KEY ( paper_id ) );""")
        
        cursor.execute("""CREATE TABLE Author(
                            author_id INT NOT NULL AUTO_INCREMENT,
                            name VARCHAR(40) NOT NULL,
                            PRIMARY KEY ( author_id ) );""")


        cursor.execute("""ALTER TABLE User
                            ADD FOREIGN KEY (publisher_id) REFERENCES Publisher(publisher_id);""")

        cursor.execute("""ALTER TABLE Periodical
                            ADD FOREIGN KEY (user_id) REFERENCES User(user_id);""")

        cursor.execute("""ALTER TABLE Periodical
                            ADD FOREIGN KEY (publisher_id) REFERENCES Publisher(publisher_id);""")

        cursor.execute("""ALTER TABLE Message
                            ADD FOREIGN KEY (user_id) REFERENCES User(user_id);""")
    
        cursor.execute("""ALTER TABLE Paper
                            ADD FOREIGN KEY (periodical_id) REFERENCES Periodical(periodical_id);""")




        cursor.execute("""CREATE TABLE BookAuthor(
                            book_id INT NOT NULL,
                            author_id INT NOT NULL,
                            PRIMARY KEY ( book_id, author_id ) );""")
        
        cursor.execute("""CREATE TABLE AuthorPaper(
                            paper_id INT NOT NULL,
                            author_id INT NOT NULL,
                            PRIMARY KEY ( paper_id, author_id ) );""")

        cursor.execute("""CREATE TABLE BookTag(
                            book_id INT NOT NULL,
                            tag_id INT NOT NULL,
                            PRIMARY KEY ( book_id, tag_id ) );""")

        cursor.execute("""CREATE TABLE PeriodicalTag(
                            periodical_id INT NOT NULL,
                            tag_id INT NOT NULL,
                            PRIMARY KEY ( periodical_id, tag_id ) );""")




        cursor.execute("""ALTER TABLE BookAuthor
                            ADD FOREIGN KEY (book_id) REFERENCES Book(book_id),
                            ADD FOREIGN KEY (author_id) REFERENCES Author(author_id);""")


        cursor.execute("""ALTER TABLE AuthorPaper
                            ADD FOREIGN KEY (paper_id) REFERENCES Paper(paper_id),
                            ADD FOREIGN KEY (author_id) REFERENCES Author(author_id);""")


        cursor.execute("""ALTER TABLE BookTag
                            ADD FOREIGN KEY (book_id) REFERENCES Book(book_id),
                            ADD FOREIGN KEY (tag_id) REFERENCES Tag(tag_id);""")


        cursor.execute("""ALTER TABLE PeriodicalTag
                            ADD FOREIGN KEY (periodical_id) REFERENCES Periodical(periodical_id),
                            ADD FOREIGN KEY (tag_id) REFERENCES Tag(tag_id);""")



@LibMS
def addUserType(cursor):
        cursor.execute("""CREATE TABLE Capacity(
                            usertype ENUM('Students', 'Faculty', 'Staff', 'Guest') NOT NULL,
                            maxbooks INT NOT NULL,
                            maxdays INT NOT NULL,
                            PRIMARY KEY ( usertype ) );""")

        cursor.execute("""ALTER TABLE User
                            ADD usertype ENUM('Students', 'Faculty', 'Staff', 'Guest') NOT NULL;""")

        cursor.execute("""ALTER TABLE User
                            ADD FOREIGN KEY (usertype) REFERENCES Capacity(usertype);""")