from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from Library_Management_System.helper.helper import *
from functools import partial
import sys
import pymysql as sql


class TableWidget(QtWidgets.QTableWidget):
    def __init__(self, parent, tablename=None, query=None):
        super(TableWidget, self).__init__(parent)
        self.tablename = tablename
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.horizontalHeader().setSortIndicatorShown(True)
        self.words = []

        if query == None and tablename != None:
            self.fillData()
        elif query != None and tablename != None:
            self.fillData(query=query)
        elif query != None and tablename == None:
            self.fillData(query=query)

    def closeDialog(self):
        self.dialog.close()
        self.parent().close()
    
    @LibMS
    def fillData(self, cursor, query=None):
        try:
            if query == None:
                cursor.execute("SELECT * FROM "+self.tablename)
            else:
                cursor.execute(query)
        except:
            self.dialog = QMessageBox(self)
            self.dialog.setIcon(QMessageBox.Critical)
            self.dialog.setText("Wrong Query detected!. Please try again with correct query.")
            self.dialog.setWindowTitle("Wrong Query!")
            self.dialog.setStandardButtons(QMessageBox.Close)
            self.dialog.buttonClicked.connect(self.closeDialog)
            self.dialog.show()
            return

        data = cursor.fetchall()
        
        if(len(data) != 0):
            self.setColumnCount(len(data[0]))
            self.setRowCount(len(data))

            for d in range(len(data)):
                for dd in range(len(data[d])):
                    self.words.append(str(data[d][dd]))
                    self.setItem(d, dd, QtWidgets.QTableWidgetItem(str(data[d][dd])))
        else:
            self.setRowCount(1)

        if(self.tablename != None):
            cursor.execute("SHOW COLUMNS FROM "+self.tablename)
            data = cursor.fetchall()
            if(len(data) != 0):
                headlist = []
                for i in range(len(data)):
                    headlist.append(data[i][0])
                    self.setHorizontalHeaderItem(i, QtWidgets.QTableWidgetItem(data[i][0]))
        self.resizeColumnsToContents()

    @pyqtSlot()
    def on_click(self):
        pass
