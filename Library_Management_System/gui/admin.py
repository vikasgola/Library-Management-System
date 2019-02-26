from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from Library_Management_System.helper.helper import *
from functools import partial
import sys
import pymysql as sql

from Library_Management_System.gui.tabwidget import TabWidget
from Library_Management_System.gui.tablewidget import TableWidget
from Library_Management_System.gui.topbarwidget import TopbarWidget
from Library_Management_System.gui.bottombarwidget import BottombarWidget

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = "Admin Panel"
        self.left = 0
        self.top = 0
        self.width = 600
        self.height = 800
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.tabnames = [t[0] for t in self.getTableNames()]
        self.tabnames.remove("BookAuthor")
        self.tabnames.remove("AuthorPaper")
        self.tabnames.remove("BookTag")
        self.tabnames.remove("PeriodicalTag")
        self.tabnames.reverse()
        self.setupUI()
        
    def setupUI(self):
        centralWidget = QWidget(self)
        self.layout = QGridLayout(centralWidget)
        self.tabWidget = TabWidget(self)
        self.topbarWidget = TopbarWidget(self)
        self.bottombarWidget = BottombarWidget(self)

        self.layout.addWidget(self.topbarWidget, 0 , 0)
        self.layout.addWidget(self.tabWidget, 1 , 0)
        self.layout.addWidget(self.bottombarWidget, 2 , 0)

        mainMenu = self.menuBar()
        exitMenu = mainMenu.addMenu("File")
        exitButton = QAction('Exit',self)
        exitButton.setShortcut('Ctrl+Q')
        exitButton.setStatusTip('Exit application')
        exitButton.triggered.connect(self.close)
        exitMenu.addAction(exitButton)

        centralWidget.setLayout(self.layout)
        self.setCentralWidget(centralWidget)
        self.show()

    @LibMS
    def getTableNames(self,cursor):
        cursor.execute("SELECT table_name FROM information_schema.tables where table_schema = '"+dbname+"';")
        return cursor.fetchall()

class UserApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = "Library Management System"
        self.left = 0
        self.top = 0
        self.width = 400
        self.height = 400
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        mainMenu = self.menuBar()
        exitMenu = mainMenu.addMenu("File")
        exitButton = QAction('Exit',self)
        exitButton.setShortcut('Ctrl+Q')
        exitButton.setStatusTip('Exit application')
        exitButton.triggered.connect(self.close)
        exitMenu.addAction(exitButton)

        self.setupUI()
        
    def setupUI(self):
        centralWidget = QWidget(self)
        self.layout = QGridLayout(centralWidget)
        userDetails = getUserDetails(_username=getLibraryUsername())
        
        # top bar 
        self.topbarWidget = QWidget(centralWidget)
        self.topbarLayout = QGridLayout(self.topbarWidget)
        self.topbarWidget.setFixedHeight(64)

        self.nameToplabel = QLabel("Name: "+userDetails["name"])
        self.nameFont = QFont()
        self.nameFont.setPointSize(20)
        self.nameToplabel.setFont(self.nameFont)
        self.topbarLayout.addWidget(self.nameToplabel, 0, 0)
        
        self.unameToplabel = QLabel("Username: "+userDetails["username"])
        self.unameFont = QFont()
        self.unameFont.setPointSize(12)
        self.unameToplabel.setFont(self.unameFont)
        self.topbarLayout.addWidget(self.unameToplabel, 1, 0)

        self.topbarWidget.setLayout(self.topbarLayout)
        self.layout.addWidget(self.topbarWidget, 0, 0)

        # middle
        queries = []
        queries.append("""SELECT Book.title, Book.pages, Book.issuetime, Book.isbn, Author.name, Publisher.name FROM Book, User, Author, Publisher, BookAuthor 
                        WHERE Book.user_id = User.user_id 
                        AND BookAuthor.book_id = Book.book_id 
                        AND BookAuthor.author_id = Author.author_id 
                        AND Publisher.publisher_id = Book.publisher_id
                        AND User.user_id = '{}'""".format(userDetails["user_id"]))
        queries.append("SELECT Message.text, Message.timestamp FROM Message WHERE Message.user_id = '{}'".format(userDetails["user_id"]))
        queries.append("""SELECT Periodical.title, Periodical.volume, Periodical.issuetime, Periodical.isbn, Publisher.name FROM Periodical, User, Publisher
                        WHERE Periodical.user_id = User.user_id
                        AND Publisher.publisher_id = Periodical.publisher_id
                        AND User.user_id = '{}'""".format(userDetails["user_id"]))
        queries.append("SELECT {} FROM Book ".format(",".join(self.getColumnNameList(tablename="Book"))))
        queries.append("SELECT {} FROM Periodical".format(",".join(self.getColumnNameList(tablename="Periodical"))))
        
        self.tabnames = [None]*5
        self.tabnamesCustom = ["Issued Book", "Message", "Issued Periodical", "Available Books", "Available Periodicals"]
        self.middleWidget = TabWidget(self, queries=queries, tabnames=self.tabnamesCustom)

        headlist = ["Title", "pages", "issuetime", "isbn", "Author Name", "Publisher Name"]
        self.middleWidget.tablist[0].layout.itemAt(0).widget().setColumnCount(len(headlist))
        for i in range(len(headlist)):
            self.middleWidget.tablist[0].layout.itemAt(0).widget().setHorizontalHeaderItem(i, QtWidgets.QTableWidgetItem(headlist[i]))
        
        headlist = ["Text", "timestamp"]
        self.middleWidget.tablist[1].layout.itemAt(0).widget().setColumnCount(len(headlist))
        for i in range(len(headlist)):
            self.middleWidget.tablist[1].layout.itemAt(0).widget().setHorizontalHeaderItem(i, QtWidgets.QTableWidgetItem(headlist[i]))
        
        headlist = ["Title", "Volume", "issuetime", "isbn", "Publisher Name"]
        self.middleWidget.tablist[2].layout.itemAt(0).widget().setColumnCount(len(headlist))
        for i in range(len(headlist)):
            self.middleWidget.tablist[2].layout.itemAt(0).widget().setHorizontalHeaderItem(i, QtWidgets.QTableWidgetItem(headlist[i]))
        
        headlist = self.getColumnNameList(tablename="Book")
        self.middleWidget.tablist[3].layout.itemAt(0).widget().setColumnCount(len(headlist))
        for i in range(len(headlist)):
            self.middleWidget.tablist[3].layout.itemAt(0).widget().setHorizontalHeaderItem(i, QtWidgets.QTableWidgetItem(headlist[i]))
        

        headlist = self.getColumnNameList(tablename="Periodical")
        self.middleWidget.tablist[4].layout.itemAt(0).widget().setColumnCount(len(headlist))
        for i in range(len(headlist)):
            self.middleWidget.tablist[4].layout.itemAt(0).widget().setHorizontalHeaderItem(i, QtWidgets.QTableWidgetItem(headlist[i]))

        self.layout.addWidget(self.middleWidget, 1, 0)

        
        centralWidget.setLayout(self.layout)
        self.setCentralWidget(centralWidget)
        self.show()

    @LibMS
    def getColumnNameList(self, cursor , tablename):
        cursor.execute("SHOW COLUMNS FROM "+tablename)
        data = cursor.fetchall()
        headlist = []
        for i in range(len(data)):
            if data[i][0] == "issuetime" or data[i][0] == "user_id":
                continue
            headlist.append(data[i][0])
        return headlist


def startLibMS():
    app = QApplication([])
    login = LoginWindow()
    if login.exec_() == QDialog.Accepted:
        if getUserMode() == "admin":
            ex = App()
            sys.exit(app.exec_())
        else:
            ex = UserApp()
            sys.exit(app.exec_())