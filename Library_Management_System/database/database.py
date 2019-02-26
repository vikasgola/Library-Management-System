import pymysql as sql
from Library_Management_System.helper.helper import *

@LibMS
def createTables(cursor):
    cursor.execute("""CREATE TABLE User(
                        user_id INT NOT NULL AUTO_INCREMENT,
                        name VARCHAR(100) NOT NULL,
                        username VARCHAR(100) NOT NULL,
                        password VARCHAR(256) NOT NULL,
                        email VARCHAR(100) NOT NULL,
                        PRIMARY KEY ( user_id ) );""")
    
    cursor.execute("""CREATE TABLE Book(
                        book_id INT NOT NULL AUTO_INCREMENT,
                        pages INT NOT NULL,
                        title TEXT NOT NULL,
                        year YEAR(4) NOT NULL,
                        isbn VARCHAR(100) NOT NULL,
                        adddate DATE NOT NULL,
                        issuetime DATETIME NULL,
                        publisher_id INT NOT NULL,
                        user_id INT NULL,
                        PRIMARY KEY ( book_id ) );""")

    cursor.execute("""CREATE TABLE Message(
                        message_id INT NOT NULL AUTO_INCREMENT,
                        text TEXT NOT NULL,
                        user_id INT NOT NULL,
                        timestamp DATETIME NOT NULL,
                        PRIMARY KEY ( message_id ) );""")

    cursor.execute("""CREATE TABLE Periodical(
                        periodical_id INT NOT NULL AUTO_INCREMENT,
                        title TEXT NOT NULL,
                        year YEAR(4) NOT NULL,
                        isbn VARCHAR(100) NOT NULL,
                        volume INT NOT NULL,
                        adddate DATE NOT NULL,
                        issuetime DATETIME NULL,
                        user_id INT NULL,
                        publisher_id INT NOT NULL, 
                        PRIMARY KEY ( periodical_id ) );""")


    cursor.execute("""CREATE TABLE Publisher(
                        publisher_id INT NOT NULL AUTO_INCREMENT,
                        name VARCHAR(100) NOT NULL,
                        PRIMARY KEY ( publisher_id ) );""")
    
    cursor.execute("""CREATE TABLE Tag(
                        tag_id INT NOT NULL AUTO_INCREMENT,
                        value VARCHAR(100) NOT NULL,
                        PRIMARY KEY ( tag_id ) );""")
    
    cursor.execute("""CREATE TABLE Paper(
                        paper_id INT NOT NULL AUTO_INCREMENT,
                        name TEXT NOT NULL,
                        periodical_id INT NOT NULL,
                        PRIMARY KEY ( paper_id ) );""")
    
    cursor.execute("""CREATE TABLE Author(
                        author_id INT NOT NULL AUTO_INCREMENT,
                        name VARCHAR(100) NOT NULL,
                        PRIMARY KEY ( author_id ) );""")


    cursor.execute("""ALTER TABLE Book
                        ADD FOREIGN KEY (user_id) REFERENCES User(user_id);""")

    cursor.execute("""ALTER TABLE Periodical
                        ADD FOREIGN KEY (user_id) REFERENCES User(user_id);""")

    cursor.execute("""ALTER TABLE Periodical
                        ADD FOREIGN KEY (publisher_id) REFERENCES Publisher(publisher_id);""")

    cursor.execute("""ALTER TABLE Message
                        ADD FOREIGN KEY (user_id) REFERENCES User(user_id);""")

    cursor.execute("""ALTER TABLE Paper
                        ADD FOREIGN KEY (periodical_id) REFERENCES Periodical(periodical_id);""")

    cursor.execute("""ALTER TABLE Book
                        ADD FOREIGN KEY (publisher_id) REFERENCES Publisher(publisher_id);""")


    cursor.execute("""CREATE TABLE ReserveBook(
                        book_id INT NOT NULL,
                        user_id INT NOT NULL,
                        PRIMARY KEY ( book_id, user_id ) );""")



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



    cursor.execute("""ALTER TABLE ReserveBook
                        ADD FOREIGN KEY (book_id) REFERENCES Book(book_id),
                        ADD FOREIGN KEY (user_id) REFERENCES User(user_id);""")



@LibMS
def addUserType(cursor):
    cursor.execute("""CREATE TABLE Capacity(
                        usertype ENUM('Students', 'Faculty', 'Staff', 'Guest') NOT NULL,
                        maxbooks INT NOT NULL,
                        maxdays INT NOT NULL,
                        PRIMARY KEY ( usertype ) );""")

    cursor.execute("""ALTER TABLE User
                        ADD usertype ENUM('Students', 'Faculty', 'Staff', 'Guest');""")


@LibMS
def addDisciplineToBook(cursor):
    cursor.execute("""CREATE TABLE Discipline(
                        book_id INT NOT NULL,
                        discipline VARCHAR(1000) NOT NULL );""")

    cursor.execute("""ALTER TABLE Discipline
                        ADD FOREIGN KEY (book_id) REFERENCES Book(book_id);""")


@LibMS
def addHistory(cursor):
    cursor.execute("""CREATE TABLE BookHistory(
                        issuedate DATE NOT NULL,
                        returndate DATE NOT NULL,
                        book_id INT NOT NULL,
                        user_id INT NOT NULL,
                        FOREIGN KEY (book_id) REFERENCES Book(book_id),
                        FOREIGN KEY (user_id) REFERENCES User(user_id),
                        PRIMARY KEY ( issuedate, returndate, book_id ) );""")

    cursor.execute("""CREATE TABLE PeriodicalHistory(
                    issuedate DATE NOT NULL,
                    returndate DATE NOT NULL,
                    periodical_id INT NOT NULL,
                    user_id INT NOT NULL,
                    FOREIGN KEY (periodical_id) REFERENCES Periodical(periodical_id),
                    FOREIGN KEY (user_id) REFERENCES User(user_id),
                    PRIMARY KEY ( issuedate, returndate, periodical_id ) );""")