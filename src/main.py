import database.database as mydb
import data.data as dg
import queries.queries as qur
import pymysql, os

def runQueries():
    qur.query1()
    qur.query2()
    qur.query3()
    qur.query4(book="Let them eat cake.")
    qur.query5(user="Otha Solis")
    qur.query7(date1="2017-06-06", date2="2018-01-01")
    qur.query9(date1="2018-01-01", date2="2018-06-01")
    qur.query10()
    qur.query11()


def buildLibMS():
    mydb.createDatabase()
    mydb.createTables()
    mydb.addUserType()
    mydb.addDisciplineToBook()
    mydb.addHistory()
    dg.addRandomDataToDB()

if __name__ == "__main__":
    try:
        runQueries()
    except:
        os.system("clear")
        mydb.clear()
        buildLibMS()    
        runQueries()
        