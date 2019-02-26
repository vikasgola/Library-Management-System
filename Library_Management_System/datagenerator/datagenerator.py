import Library_Management_System.database.database as db
from Library_Management_System.helper.helper import *
import random,copy, datetime
from mimesis import Person, Business, Text, Numbers, Datetime, Code
import mimesis as dgen

ut = ["Students","Students","Students","Students","Students","Students", "Faculty","Faculty", "Faculty", "Staff", "Staff", "Guest","Guest","Guest"]
authors = []
publisher = []
tags = []
messages = []
users = []
books = []
periodicals = []
capacity = []
papers = []
bookauthor =[]
authorpaper = []
booktag =[]
periodicaltag = []
bhistory = []
phistory = []
discipline = []

@LibMS
def addtoDataBase(cursor, tablename, data):
    for d in data:
        placeholders = ', '.join(['%s'] * len(d))
        columns = ', '.join(d.keys())
        q = "INSERT INTO %s ( %s ) VALUES ( %s )" % (tablename, columns, placeholders)
        cursor.execute(q, list(d.values()))

def createData(num):
    # authors
    for i in range(random.randint(num//4, num*4)):
        authors.append({
            "name": Person().full_name()
        })

    # publisher
    for i in range(random.randint(num//4, num*4)):
        publisher.append({
            "name": Business().company()
        })
    
    # tag
    for i in range(random.randint(num//4, num*4)):
        tags.append({
            "value": Text().word()
        })
    
    # users
    for i in range(random.randint(num//4, num)):
        users.append({
            "name": Person().full_name(),
            "password": Person().password(),
            "username": Person().username(),
            "email": Person().email(),
            "usertype": random.choice(ut),
        })

    # messages
    for i in range(random.randint(num//2, num*8)):
        messages.append({
            "text": Text().sentence(),
            "user_id": Numbers().between(minimum=1, maximum=len(users)),
            "timestamp": Datetime().datetime(start=2016,end=2018)
        })

    # books
    for i in range(random.randint(num//4, num*4)):
        if random.random() < 0.4:
            books.append({
                "pages": Numbers().between(minimum=100, maximum=1000),
                "title": Text().quote(),
                "year": Datetime().year(minimum=2013, maximum=2018),
                "isbn" : Code().isbn(),
                "adddate": Datetime().date(start=2013, end=2018),
                # "issuetime": "NULL",
                "publisher_id": Numbers().between(minimum=1, maximum=len(publisher)),
                # "user_id": "NULL"
            })
        else:
            opendate = Datetime().year(minimum=2013, maximum=2018)
            adddate = Datetime().date(start=opendate, end=2018)
            books.append({
                "pages": Numbers().between(minimum=100, maximum=1000),
                "title": Text().quote(),
                "year": opendate,
                "isbn" : Code().isbn(),
                "adddate": adddate,
                "issuetime": Datetime().datetime(start=adddate.year, end=2018),
                "publisher_id": Numbers().between(minimum=1, maximum=len(publisher)),
                "user_id": Numbers().between(minimum=1, maximum=len(users))
            })

    # Periodical
    for i in range(random.randint(num//4, num*4)):
        if random.random() < 0.4:
            periodicals.append({
                "title": Text().quote(),
                "year": Datetime().year(minimum=2013, maximum=2018),
                "isbn" : Code().isbn(),
                "adddate": Datetime().date(start=2013, end=2018),
                # "issuetime": "NULL",
                "publisher_id": Numbers().between(minimum=1, maximum=len(publisher)),
                # "user_id": "NULL",
                "volume": Numbers().between(minimum=1, maximum=10)
            })
        else:
            opendate = Datetime().year(minimum=2013, maximum=2018)
            adddate = Datetime().date(start=opendate, end=2018)
            periodicals.append({
                "title": Text().quote(),
                "year": opendate,
                "isbn" : Code().isbn(),
                "adddate": adddate,
                "issuetime": Datetime().datetime(start=adddate.year, end=2018),
                "publisher_id": Numbers().between(minimum=1, maximum=len(publisher)),
                "user_id": Numbers().between(minimum=1, maximum=len(users)),
                "volume": Numbers().between(minimum=1, maximum=10)
            })

    # papers
    for i in range(random.randint(num//4, num*2)):
        papers.append({
            "name": Text().quote(),
            "periodical_id": Numbers().between(minimum=1, maximum=len(periodicals))
        })

    # book author
    for i in range(len(books)):
        bookauthor.append({
            "book_id": i+1,
            "author_id": Numbers().between(minimum=1, maximum=len(authors))
        })


    # paper author
    for i in range(len(papers)):
        authorpaper.append({
            "paper_id": i+1,
            "author_id": Numbers().between(minimum=1, maximum=len(authors))
        })

    # book tag
    for i in range(len(books)):
        booktag.append({
            "book_id": i+1,
            "tag_id": Numbers().between(minimum=1, maximum=len(tags))
        })

    # periodical tag
    for i in range(len(periodicals)):
        periodicaltag.append({
            "periodical_id": i+1,
            "tag_id": Numbers().between(minimum=1, maximum=len(tags))
        })


    # book history tag
    for i in range(random.randint(num, num*4)):
        boid = Numbers().between(minimum=1, maximum = len(books))
        issd = Datetime().date(start=books[boid-1]["adddate"].year, end=2018)
        retd = Datetime().date(start=issd.year, end=2018)
        bhistory.append({
            "issuedate": issd,
            "returndate": retd,
            "book_id": boid,
            "user_id": Numbers().between(minimum=1, maximum = len(users)),
        })

    # periodical history tag
    for i in range(random.randint(num, num*4)):
        boid = Numbers().between(minimum=1, maximum = len(periodicals))
        issd = Datetime().date(start=periodicals[boid-1]["adddate"].year, end=2018)
        retd = Datetime().date(start=issd.year, end=2018)
        phistory.append({
            "issuedate": issd,
            "returndate": retd,
            "periodical_id": boid,
            "user_id": Numbers().between(minimum=1, maximum = len(users)),
        })

    temp = ['Students', 'Faculty', 'Staff', 'Guest']
    mb = [3, 6, 4, 2]
    md = [15, 30, 30, 7]
    for i in range(4):
        capacity.append({
            "usertype": temp[i],
            "maxbooks": mb[i],
            "maxdays" : md[i],
        })

    # discipline
    for i in range(len(books)):
        discipline.append({
            "discipline": Text().word(),
            "book_id": i+1,
        })


def addAllData():
    addtoDataBase(tablename="User", data=users)
    addtoDataBase(tablename="Publisher", data=publisher)
    addtoDataBase(tablename="Author", data=authors)
    addtoDataBase(tablename="Book", data=books)
    addtoDataBase(tablename="Periodical", data=periodicals)
    addtoDataBase(tablename="Message", data=messages)
    addtoDataBase(tablename="Paper", data=papers)
    addtoDataBase(tablename="Tag", data=tags)

    addtoDataBase(tablename="BookAuthor", data=bookauthor)
    addtoDataBase(tablename="BookTag", data=booktag)
    addtoDataBase(tablename="AuthorPaper", data=authorpaper)
    addtoDataBase(tablename="PeriodicalTag", data=periodicaltag)

    addtoDataBase(tablename="BookHistory", data=bhistory)
    addtoDataBase(tablename="PeriodicalHistory", data=phistory)
    addtoDataBase(tablename="Capacity", data=capacity)
    addtoDataBase(tablename="Discipline", data=discipline)


def addRandomDataToDB(num=100):
    createData(num)
    addAllData()


def buildLibMS():
    db.createTables()
    db.addUserType()
    db.addDisciplineToBook()
    db.addHistory()
    addRandomDataToDB(200)