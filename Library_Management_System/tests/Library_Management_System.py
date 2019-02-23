import Library_Management_System.database.database as mydb
import Library_Management_System.data.data as dg
import Library_Management_System.queries.queries as qur
import Library_Management_System.gui.gui as gui
import sys

def runQueries():
    qur.query1()
    qur.query2()
    qur.query3()
    qur.query4(book="Let them eat cake.")
    qur.query5(user="Shad Becker")
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
    dg.addRandomDataToDB(200)

if __name__ == "__main__":
    if(len(sys.argv) > 1 and sys.argv[1] == "clear"):
        mydb.clear()
    elif len(sys.argv) > 1 and sys.argv[1] == "makedb":
        buildLibMS()
    else:
        try:
            runQueries()
            gui.startLibMS()
        except:
            buildLibMS()
            runQueries()
            gui.startLibMS()

