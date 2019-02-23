from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from Library_Management_System.helper.helper import *
from functools import partial
import sys
import pymysql as sql

from Library_Management_System.gui.tabwidget import TabWidget
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
        self.layout = QGridLayout(self)
        self.tabWidget = TabWidget(self)
        self.topbarWidget = TopbarWidget(self)
        self.bottombarWidget = BottombarWidget(self)

        self.layout.addWidget(self.topbarWidget, 0 , 0)
        self.layout.addWidget(self.tabWidget, 1 , 0)
        self.layout.addWidget(self.bottombarWidget, 2 , 0)

        centralWidget.setLayout(self.layout)
        self.setCentralWidget(centralWidget)
        self.show()

    @LibMS
    def getTableNames(self,cursor):
        cursor.execute("SELECT table_name FROM information_schema.tables where table_schema = '"+dbname+"';")
        return cursor.fetchall()


def startLibMS():
    app = QApplication([])
    login = LoginWindow()
    if login.exec_() == QDialog.Accepted:
        ex = App()
        sys.exit(app.exec_())