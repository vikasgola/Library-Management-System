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
history = []

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
    for i in range(random.randint(num//4, num*4)):
        users.append({
            "name": Person().full_name(),
            "password": Person().password(),
            "username": Person().username(),
            "email": Person().email(),
            "usertype": random.choice(ut) 
        })

    # messages
    for i in range(random.randint(num//2, num*8)):
        messages.append({
            "text": Text().sentence(),
            "user_id": Numbers().between(minimum=1, maximum=num),
            "timestamp": Datetime().datetime()
        })
    
    # books
    for i in range(random.randint(num//4, num*4)):
        if random.random() < 0.4:
            books.append({
                "pages": Numbers().between(minimum=100, maximum=1000),
                "title": Text().quote(),
                "year": Datetime().year(minimum=2013, maximum=2018),
                "isbn" : Code().isbn(),
                "adddate": Datetime().date(),
                # "issuetime": Datetime().datetime(),
                "publisher_id": Numbers().between(minimum=1, maximum=num//2),
                # "user_id": Numbers().between(minimum=1, maximum=num)
            })
        else:
            books.append({
                "pages": Numbers().between(minimum=100, maximum=1000),
                "title": Text().quote(),
                "year": Datetime().year(minimum=2013, maximum=2018),
                "isbn" : Code().isbn(),
                "adddate": Datetime().date(),
                "issuetime": Datetime().datetime(),
                "publisher_id": Numbers().between(minimum=1, maximum=num//2),
                "user_id": Numbers().between(minimum=1, maximum=num)
            })

    # Periodical
    for i in range(random.randint(num//4, num*4)):
        if random.random() < 0.4:
            periodicals.append({
                "title": Text().quote(),
                "year": Datetime().year(minimum=2013, maximum=2018),
                "isbn" : Code().isbn(),
                "adddate": Datetime().date(),
                # "issuetime": Datetime().datetime(),
                "publisher_id": Numbers().between(minimum=1, maximum=num//2),
                # "user_id": Numbers().between(minimum=1, maximum=num),
                "volume": Numbers().between(minimum=1, maximum=10)
            })
        else:
            periodicals.append({
                "title": Text().quote(),
                "year": Datetime().year(minimum=2013, maximum=2018),
                "isbn" : Code().isbn(),
                "adddate": Datetime().date(),
                "issuetime": Datetime().datetime(),
                "publisher_id": Numbers().between(minimum=1, maximum=num//2),
                "user_id": Numbers().between(minimum=1, maximum=num),
                "volume": Numbers().between(minimum=1, maximum=10)
            })

    # papers
    for i in range(random.randint(num//4, num*2)):
        papers.append({
            "name": Text().quote(),
            "periodical_id": Numbers().between(minimum=1, maximum=num*int(1.5))
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


    # history tag
    for i in range(random.randint(num, num*10)):
        issd = Datetime().date()
        retd = copy.copy(issd) + datetime.timedelta(days= Numbers().between(minimum=2, maximum=60))
        history.append({
            "issuedate": issd,
            "returndate": retd,
            "book_id": Numbers().between(minimum=1, maximum = len(books)),
            "user_id": Numbers().between(minimum=1, maximum = len(users)),
        })

    # capacity
    # for i in range(num*int(1.5)):
    #     capacity.append({
    #         "title": Text.title(),
    #         "year": Datetime.year(minimum=2013, maximum=2018),
    #         "isbn" : Code().isbn(),
    #         "adddate": Datetime.date(),
    #         "issuetime": Datetime.datetime(),
    #         "publisher_id": Numbers.between(minimum=1, maximum=num//2),
    #         "user_id": Numbers.between(minimum=1, maximum=num)
    #     })



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

    addtoDataBase(tablename="History", data=history)



def addRandomDataToDB(num=100):
    createData(num)
    addAllData()