import pymysql as sql
import getpass
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import pymysql as sql
import getpass

username = None
password = None
dbname = "LibMS"
usermode = "admin"
libraryUsername = None

def LibMS(func):
    def inner(*args, **kwargs):
        connection = sql.connect(host='localhost', user=username, password=password, database=dbname)
        try:
            with connection.cursor() as cursor:
                out = func(*args, **kwargs, cursor=cursor)
            connection.commit()
        finally:
            connection.close()
        return out
    return inner

class LoginWindow(QDialog):
    def __init__(self, parent=None):
        super(LoginWindow, self).__init__(parent)
        self.papa = parent
        self.setFixedWidth(400)
        self.setFixedHeight(280)

        self.setWindowTitle("Library Management System")
        self.layout = QFormLayout(self)

        self.note = QLabel("Admin Login")
        self.font = QFont()
        self.font.setPointSize(32)
        self.font.setBold(True)
        self.note.setFont(self.font)
        self.note.setContentsMargins(10,20, 10, 30)
        self.note.setAlignment(Qt.AlignCenter)
        self.layout.addRow(self.note)

        self.font2 = QFont()
        self.font2.setPointSize(13)
        

        self.namelabel = QLabel("Name: ")
        self.namefield = QLineEdit(self)
        self.namefield.setFont(self.font2)
        self.namelabel.setFont(self.font2)
        self.layout.addRow(self.namelabel, self.namefield)
        self.namelabel.hide()
        self.namefield.hide()

        self.emaillabel = QLabel("Email: ")
        self.emailfield = QLineEdit(self)
        self.emailfield.setFont(self.font2)
        self.emaillabel.setFont(self.font2)
        self.layout.addRow(self.emaillabel, self.emailfield)
        self.emailfield.hide()
        self.emaillabel.hide()

        self.utypelabel = QLabel("UserType: ")
        self.utypefield = QComboBox(self)
        self.utypefield.addItem("Faculty")
        self.utypefield.addItem("Guest")
        self.utypefield.addItem("Students")
        self.utypefield.addItem("Staff")
        self.utypefield.setFont(self.font2)
        self.utypelabel.setFont(self.font2)
        self.layout.addRow(self.utypelabel, self.utypefield)
        self.utypefield.hide()
        self.utypelabel.hide()


        self.userlabel = QLabel("Username: ")
        self.userfield = QLineEdit(self)
        self.userfield.setFont(self.font2)
        self.userlabel.setFont(self.font2)
        reg = QRegExp("[\S]+")
        input_validator = QRegExpValidator(reg, self.userfield)
        self.userfield.setValidator(input_validator)  
        self.layout.addRow(self.userlabel, self.userfield)

        self.passlabel = QLabel("Password: ")
        self.passfield = QLineEdit(self)
        self.passfield.setFont(self.font2)
        self.passlabel.setFont(self.font2)
        self.passfield.setEchoMode((QLineEdit.Password))
        self.layout.addRow(self.passlabel, self.passfield)

        self.submit = QPushButton("Login")
        self.submit.setFixedWidth(100)
        self.cancel = QPushButton("Cancel")
        self.submit.setFont(self.font2)
        self.cancel.setFont(self.font2)
        self.cancel.clicked.connect(lambda: (self.reject(), self.close()))
        self.submit.clicked.connect(self.handleLogin)
        self.layout.addRow(self.submit, self.cancel)
        
        self.notadmin = QPushButton("Not Admin?")
        self.notadmin.setMinimumWidth(120)
        self.terms = QLabel("terms & condition")
        self.font3 = QFont()
        self.font3.setUnderline(True)
        self.terms.setFont(self.font3)
        self.notadmin.clicked.connect(self.handleUserMode)
        self.terms.setAlignment(Qt.AlignCenter)
        self.layout.addRow(self.notadmin, self.terms)
        
        self.layout.setAlignment(Qt.AlignVCenter)
        self.setLayout(self.layout)
        
    def handleUserMode(self):
        setUsername("lmsuser")
        setPassword("lmsuserpassword")

        self.setFixedHeight(280)
        self.namelabel.hide()
        self.namefield.hide()
        self.utypefield.hide()
        self.utypelabel.hide()
        self.emailfield.hide()
        self.emaillabel.hide()

        
        global usermode
        usermode = "user"
        self.note.setText("User Login")
        self.notadmin.setText("Not Registered?")
        self.notadmin.clicked.disconnect()
        self.notadmin.clicked.connect(self.handleSignUpMode)
        self.submit.setText("Login")
        self.submit.clicked.disconnect()
        self.submit.clicked.connect(self.handleLogin)

    def handleSignUpMode(self):
        self.namelabel.show()
        self.namefield.show()
        self.utypefield.show()
        self.utypelabel.show()
        self.emailfield.show()
        self.emaillabel.show()

        self.notadmin.setText("Already Have \nan Account?")
        self.notadmin.clicked.disconnect()
        self.notadmin.clicked.connect(self.handleUserMode)
        self.submit.setText("Sign Up!")
        self.submit.clicked.disconnect()
        self.submit.clicked.connect(self.handleSignUp)
        self.setFixedHeight(400)

    
    @LibMS
    def checkForExist(self, cursor, _username):
        cursor.execute("SELECT username FROM User;")
        usernames = cursor.fetchall()
        for localu in usernames:
            if _username == localu[0]:
                return True
        return False

    def handleSignUp(self):
        query = "INSERT INTO User (name, username, password, email, usertype) VALUES ("
        query += ' "'+self.namefield.text()+'",'
        query += ' "'+self.userfield.text()+'",'
        query += ' "'+self.passfield.text()+'",'
        query += ' "'+self.emailfield.text()+'",'
        query += ' "'+self.utypefield.currentText()+'" )'

        try:
            if(self.namefield.text() == "" or self.userfield.text() == "" or self.passfield.text() == "" or self.emailfield.text() == ""):
                raise Exception("Fields Blank!")
            if not self.checkForExist(_username=self.userfield.text()):
                self.runQuery(quer=query)
                self.dialog = QMessageBox(self)
                self.dialog.setIcon(QMessageBox.Information)
                self.dialog.setText("Congratulations.\nSuccesfully Sign Up!")
                self.dialog.setWindowTitle("Succesfull!")
                self.dialog.setStandardButtons(QMessageBox.Close)
                self.dialog.buttonClicked.connect(self.dialog.close)
                self.dialog.show()
                self.namefield.clear()
                self.userfield.clear()
                self.passfield.clear()
                self.emailfield.clear()
            else:
                raise Exception("Username Exist!")
        except:
            self.dialog2 = QMessageBox(self)
            self.dialog2.setIcon(QMessageBox.Critical)
            self.dialog2.setText("Incorrect Input Data or Username Already Exist. Try Again!")
            self.dialog2.setWindowTitle("Can't Add You!")
            self.dialog2.setStandardButtons(QMessageBox.Close)
            self.dialog2.buttonClicked.connect(self.dialog2.close)
            self.dialog2.show()


    @LibMS
    def runQuery(self, cursor, quer):
        cursor.execute(quer)

    def handleLogin(self):
        try:
            global usermode, libraryUsername
            global username, password

            if usermode == "user":
                connection = sql.connect(host='localhost', user=username, password=password, database=dbname)
                libraryUsername = self.userfield.text()
                connection.close()
            else:
                connection = sql.connect(host='localhost', user=self.userfield.text(), password=self.passfield.text(), database=dbname)
                setUsername(self.userfield.text())
                setPassword(self.passfield.text())
                connection.close()

            if self.checkUser() or usermode == "admin":
                self.accept()
                self.close()
            else:
                raise Exception("Wrong User Name or Password!")
        except:
            self.dialog = QMessageBox(self)
            self.dialog.setIcon(QMessageBox.Critical)
            self.dialog.setText("Wrong User Name or Password or Incomplete Data!. Try Again!")
            self.dialog.setWindowTitle("Error!")
            self.dialog.setStandardButtons(QMessageBox.Close)
            self.dialog.buttonClicked.connect(lambda: (
                self.dialog.close()
                )
            )
            self.dialog.show()
        finally:
            self.userfield.clear(),
            self.passfield.clear()

    @LibMS
    def checkUser(self, cursor):
        _username = self.userfield.text()
        _password = self.passfield.text()

        cursor.execute("SELECT username, password FROM User;")
        data = cursor.fetchall()
        for localu in data:
            if _username == localu[0] and _password == localu[1]:
                return True
        return False


@LibMS
def getUserDetails(cursor, _username):
    userDetails = {}
    cursor.execute("SELECT user_id, name, username, email FROM User WHERE User.username = '"+_username+"' ;")
    data = cursor.fetchall()
    if( len(data) > 0):
        data = data[0]
    else:
        returns
    userDetails["user_id"] = data[0]
    userDetails["name"] = data[1]
    userDetails["username"] = data[2]
    userDetails["email"] = data[3]
    return userDetails

def setUsername(_username):
    global username
    username = _username

def setPassword(_password):
    global password
    password = _password

def getLibraryUsername():
    global libraryUsername
    return libraryUsername

def getUserMode():
    global usermode
    return usermode