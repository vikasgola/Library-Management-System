import Library_Management_System.datagenerator.datagenerator as d
import Library_Management_System.helper.helper as hel
import pymysql as sql
import getpass

def createDatabase(username,password):
    connection = sql.connect(host='localhost', user=username, password=password)
    try:
        with connection.cursor() as cursor:
            cursor.execute("CREATE DATABASE LibMS;")
        connection.commit()
    except:
        raise Exception("Failed to Create Database.")
    finally:
        connection.close()
    
def clear(username,password):
    connection = sql.connect(host='localhost', user=username, password=password)
    try:
        with connection.cursor() as cursor:
            cursor.execute("drop database LibMS;")
        connection.commit()
    finally:
        connection.close()

def createUser(username,password):
    connection = sql.connect(host='localhost', user=username, password=password)
    try:
        with connection.cursor() as cursor:
            print("Set Admin Username and Password for LibMS.")
            _username = input("Username: ")
            _password = getpass.getpass("Password: ")
            while(_username == "" or _password == ""):
                print("Username or Password can't be set to Blank.")
                _username = input("Username: ")
                _password = getpass.getpass("Password: ")
            try:    
                cursor.execute("DROP USER '{}'@'localhost'".format(_username))
                cursor.execute("DROP USER '{}'@'localhost';".format("lmsuser"))
            except:
                cursor.execute("CREATE USER '{}'@'localhost' IDENTIFIED BY '{}';".format(_username, _password))
                cursor.execute("GRANT ALL PRIVILEGES ON LibMS.* To '{}'@'localhost' IDENTIFIED BY '{}';".format(_username, _password))
                cursor.execute("CREATE USER '{}'@'localhost' IDENTIFIED BY '{}';".format("lmsuser","lmsuserpassword"))
                cursor.execute("GRANT SELECT, INSERT, UPDATE ON LibMS.* To '{}'@'localhost' IDENTIFIED BY '{}';".format("lmsuser", "lmsuserpassword"))
        connection.commit()
    except:
        raise Exception("Failed to Create User")
    finally:
        connection.close()


if __name__ == "__main__":
    print("")
    print("Library Management System (LibMS) need username and Password to create Database for it.")
    username = input("Username(mysql): ")
    password = getpass.getpass("Password(mysql): ")

    hel.setUsername(username)
    hel.setPassword(password)
    
    print("Creating Database.")
    try:
        createDatabase(username,password)
    except:
        clear(username,password)
        createDatabase(username,password)
    print("Database created.")

    print("Creating Admin User for LibMS")
    createUser(username,password)
    print("Creating Admin User for LibMS")


    print("Adding Random Data to Database.")
    d.buildLibMS()
    print("Data added!")