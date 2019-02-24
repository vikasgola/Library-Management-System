from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from Library_Management_System.helper.helper import *
from functools import partial
import sys
import pymysql as sql

from Library_Management_System.gui.tablewidget import TableWidget

class QueryWindow(QMainWindow):
    def __init__(self, parent, query):
        super(QueryWindow, self).__init__(parent)
        self.setWindowTitle("Query Output")
        tableWidget = TableWidget(self, query=query)
        self.setCentralWidget(tableWidget)

class TopbarWidget(QWidget):
    def __init__(self, parent):
        super(TopbarWidget, self).__init__(parent)
        self.layout = QHBoxLayout(self)
        self.setFixedHeight(64)
        self.papa = parent

        self.searchBar = QTextEdit()
        self.searchBar.setPlaceholderText("Write Your 'SELECT' Query!")
        self.searchBar.setFixedHeight(48)
        font = QFont()
        font.setPointSize(14)
        self.searchBar.setFont(font)
        self.layout.addWidget(self.searchBar)

        self.btn1 = QPushButton(self)
        self.btn1.setText("Query!")
        font2 = QFont()
        font2.setPointSize(11)
        self.btn1.setFont(font2)
        self.btn1.setFixedHeight(48)

        self.btn1.clicked.connect(self.handleSeachBar)
        self.layout.addWidget(self.btn1)
        self.setLayout(self.layout)

    def handleSeachBar(self):
        if( (("SELECT" in self.searchBar.toPlainText()) 
            or ("select" in self.searchBar.toPlainText()))
            and ("insert" not in self.searchBar.toPlainText())
            and ("drop" not in self.searchBar.toPlainText())
            and ("alter" not in self.searchBar.toPlainText())
            and ("create" not in self.searchBar.toPlainText())):
            self.queryWindow = QueryWindow(self.papa, self.searchBar.toPlainText())
            self.queryWindow.show()
        else:
            self.queryWindow.close()
            self.dialog = QMessageBox(self)
            self.dialog.setIcon(QMessageBox.Critical)
            self.dialog.setText("Not SELECT query!. Only SELECT queries can be used. Please Try Again with SELECT query.")
            self.dialog.setWindowTitle("Not SELECT query!")
            self.dialog.setStandardButtons(QMessageBox.Close)
            self.dialog.buttonClicked.connect(self.dialog.close)
            self.dialog.show()
