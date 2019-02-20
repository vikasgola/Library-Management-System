import database.database as mydb
import data.data as dg

if __name__ == "__main__":
    mydb.createDatabase()
    mydb.createTables()
    mydb.addUserType()
    mydb.addDisciplineToBook()
    mydb.addHistory()
    dg.addRandomDataToDB()
    
