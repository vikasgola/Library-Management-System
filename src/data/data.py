import sys
sys.path.append('../')
from helper.helper import LibMS

import random
from mimesis import Person, Business, Text, Numbers, Datetime, Code
import mimesis as dgen

dbname = "LibMS"
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

@LibMS
def addtoDataBase(cursor, tablename, data):
    for d in data:
        placeholders = ', '.join(['%s'] * len(d))
        columns = ', '.join(d.keys())
        q = "INSERT INTO %s ( %s ) VALUES ( %s )" % (tablename, columns, placeholders)
        cursor.execute(q, list(d.values()))

def createData(num=100):
    # authors
    for i in range(num//2):
        authors.append({
            "name": Person().full_name()
        })

    # publisher
    for i in range(num//2):
        publisher.append({
            "name": Business().company()
        })
    
    # tag
    for i in range(num//2):
        tags.append({
            "value": Text().word()
        })
    
    # users
    for i in range(num):
        users.append({
            "name": Person().full_name(),
            "password": Person().password(),
            "username": Person().username(),
            "email": Person().email(),
            "usertype": random.choice(ut) 
        })

    # messages
    for i in range(num*2):
        messages.append({
            "text": Text().sentence(),
            "user_id": Numbers().between(minimum=1, maximum=num),
            "timestamp": Datetime().datetime()
        })
    
    # books
    for i in range(num*2):
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
    for i in range(num*int(1.5)):
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
    for i in range(num*int(1.5)//2):
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

if __name__ == "__main__":
    createData()
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
