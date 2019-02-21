import pymysql as sql

dbname = "LibMS"
def LibMS(func):
    def inner(*args, **kwargs):
        connection = sql.connect(host='localhost', user='lms', password="openlibrary", database=dbname)
        try:
            with connection.cursor() as cursor:
                out = func(*args, **kwargs, cursor=cursor)
            connection.commit()
            return out
        finally:
            connection.close()
    return inner