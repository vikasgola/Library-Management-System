import pymysql as sql
import getpass
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from Library_Management_System.helper.helper import *

username = None
password = None
dbname = "LibMS"
usermode = None

class LoginWindow(QDialog):
    def __init__(self, parent=None):
        super(LoginWindow, self).__init__(parent)
        self.papa = parent
        self.setFixedWidth(400)
        self.setFixedHeight(240)

        self.setWindowTitle("Library Management System")
        self.layout = QFormLayout(self)

        usermode = "Admin"
        self.note = QLabel("Admin Login")
        self.font = QFont()
        self.font.setPointSize(24)
        self.font.setBold(True)
        self.note.setFont(self.font)
        self.note.setContentsMargins(10,20, 10, 30)
        self.note.setAlignment(Qt.AlignCenter)
        self.layout.addRow(self.note)

        self.font2 = QFont()
        self.font2.setPointSize(13)

        self.userlabel = QLabel("Username: ")
        self.userfield = QLineEdit(self)
        self.userfield.setFont(self.font2)
        self.userlabel.setFont(self.font2)
        self.layout.addRow(self.userlabel, self.userfield)

        self.passlabel = QLabel("Password: ")
        self.passfield = QLineEdit(self)
        self.passfield.setFont(self.font2)
        self.passlabel.setFont(self.font2)
        self.passfield.setEchoMode((QLineEdit.Password))
        self.layout.addRow(self.passlabel, self.passfield)

        self.submit = QPushButton("Login")
        self.cancel = QPushButton("Cancel")
        self.submit.setFont(self.font2)
        self.cancel.setFont(self.font2)
        self.cancel.clicked.connect(self.handleCancel)
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
        global usermode
        usermode = "user"
        self.note.setText("User Login")
        self.notadmin.setText("Sign Up")
    
    def signUp(self):
        pass
    
    def handleCancel(self):
        self.reject()

    def handleLogin(self):
        try:
            global usermode
            global username, password
            
            if username == "user":
                username = "lmsuser"
                password = "lmsuserpassword"
                connection = sql.connect(host='localhost', user=username, password=password, database=dbname)
                connection.close()
            else:
                connection = sql.connect(host='localhost', user=self.userfield.text(), password=self.passfield.text(), database=dbname)
                connection.close()

            username = self.userfield.text()
            password = self.passfield.text()
            if self.checkUser():
                self.accept()
                self.close()
            else:
                raise Exception("Wrong User Name or Password!")
        except:
            QMessageBox.warning(self, 'Error', 'Wrong Username or Password!')
            self.userfield.clear()
            self.passfield.clear()

    def checkUser(self):
        return True

def LibMS(func):
    def inner(*args, **kwargs):
        connection = sql.connect(host='localhost', user=username, password=password, database=dbname)
        try:
            with connection.cursor() as cursor:
                out = func(*args, **kwargs, cursor=cursor)
            connection.commit()
            return out
        finally:
            connection.close()
    return inner