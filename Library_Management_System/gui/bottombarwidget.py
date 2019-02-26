from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from Library_Management_System.helper.helper import *
from functools import partial
import sys
import pymysql as sql

from Library_Management_System.gui.formwidget import FormDialog
from Library_Management_System.gui.tabwidget import TabWidget


class BottombarWidget(QWidget):
    def __init__(self, parent, addbutton=True):
        super(BottombarWidget, self).__init__(parent)
        self.layout = QHBoxLayout(self)
        self.addSearchBar(parent)
        self.papa = parent

    
        self.btn1 = QPushButton(self)
        self.btn1.setText("Add Data")
        self.btn1.setFixedWidth(100)
        self.btn1.clicked.connect(self.handleAddButton)
        self.layout.addWidget(self.btn1, 8, Qt.AlignRight)
        
        self.btn3 = QPushButton(self)
        self.btn3.setText("Update Data")
        self.btn3.setFixedWidth(100)
        self.btn3.clicked.connect(self.handleUpdateButton)
        self.layout.addWidget(self.btn3, 1, Qt.AlignRight)
    
        self.btn2 = QPushButton(self)
        self.btn2.setText("Delete Data")
        self.btn2.setFixedWidth(100)
        self.btn2.clicked.connect(self.handleDeleteButton)
        self.layout.addWidget(self.btn2, 0, Qt.AlignRight)

        self.setLayout(self.layout)

    def addSearchBar(self, parent):
        self.searchBar = QLineEdit()
        self.searchBar.setPlaceholderText("Search Anything!")
        model = QStringListModel()
        index = parent.tabWidget.currentIndex()
        words = parent.tabWidget.widget(index).layout.itemAt(0).widget().words
        model.setStringList(words)

        completer = QCompleter()
        completer.setModel(model)
        self.searchBar.setCompleter(completer)
        self.layout.addWidget(self.searchBar, 0, Qt.AlignLeft)

        self.searchbtn = QPushButton(self)
        self.searchbtn.setIcon(QIcon('search.png'))
        self.searchbtn.setIconSize(QSize(18,18))
        self.searchbtn.clicked.connect(self.handleSeachBar)
        self.layout.addWidget(self.searchbtn , 1, Qt.AlignLeft)

    def handleSeachBar(self):
        searchtext = self.searchBar.text()
        searchedWindow = SearchedWindow(self.papa, searchtext)
        searchedWindow.show()

    def handleUpdateButton(self):
        index = self.papa.tabWidget.currentIndex()
        tabWidget = self.papa.tabWidget.widget(index).layout.itemAt(0).widget()
        selectedRows = [idx.row() for idx in tabWidget.selectionModel().selectedRows()]
        self.dialog = QMessageBox(self)
        self.dialog.setIcon(QMessageBox.Warning)
        if len(selectedRows) > 1:
            self.dialog.setText("Only 1 Row can be selected for Update Purpose.")
            self.dialog.setStandardButtons( QMessageBox.Ok)
            self.dialog.setWindowTitle("updation")
            retval = self.dialog.exec_()
            if retval == QMessageBox.Ok:
                self.dialog.close()
                return
        elif len(selectedRows) == 0:
            self.dialog.setText("No Row was selected. Please select a row.")
            self.dialog.setStandardButtons( QMessageBox.Close)
            self.dialog.setWindowTitle("updation")
            retval = self.dialog.exec_()
            if retval == QMessageBox.Close:
                self.dialog.close()
                return

        inputfield = self.getColumnNameListExceptPrimaryKey(tablename=self.papa.tabnames[index])
        data = []
        allcol = self.getColumnNameList(tablename=self.papa.tabnames[index])
        for i in range(len(allcol)):
            if allcol[i] not in inputfield:
                continue
            data.append(tabWidget.item(selectedRows[0], i).text())
        assert(len(inputfield) == len(data))

        self.updateform = FormDialog(self, inputnamelist=inputfield, tablename=self.papa.tabnames[index], update=True, dataToFill=data)
        self.updateform.show()
        
    def handleAddButton(self):
        self.buttonbox = QDialog(self)
        self.buttonbox.setFixedWidth(200)
        self.layout = QVBoxLayout(self.buttonbox)

        self.buttons = []
        self.inputfields = []
        self.forms = []
        for i in range(len(self.papa.tabnames)):
            self.buttons.append(QPushButton(self.buttonbox))
            self.buttons[i].setText("Add "+self.papa.tabnames[i])
            inputfield = self.getColumnNameListExceptPrimaryKey(tablename=self.papa.tabnames[i])
            self.inputfields.append(inputfield)
            self.forms.append(FormDialog(self, inputnamelist=self.inputfields[i], tablename=self.papa.tabnames[i]))
            self.forms[i].setWindowTitle("Add new "+self.papa.tabnames[i])
            self.buttons[i].clicked.connect(partial(self.handleChildAddButton, self.forms[i]))
            self.layout.addWidget(self.buttons[i])

        cancelbtn = QPushButton(self.buttonbox)
        cancelbtn.setText("Cancel")
        cancelbtn.clicked.connect(lambda: self.buttonbox.close())
        self.layout.addWidget(cancelbtn)

        self.buttonbox.setLayout(self.layout)
        self.buttonbox.show()

    @LibMS
    def getColumnNameListExceptPrimaryKey(self, cursor , tablename):
        q = """SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE TABLE_SCHEMA = '{}'
                AND TABLE_NAME = '{}'    
                AND (COLUMN_KEY != 'PRI' OR COLUMN_NAME NOT LIKE '%id%');""".format(dbname, tablename)
        cursor.execute(q)
        data = cursor.fetchall()
        headlist = []
        for i in range(len(data)):
            headlist.append(data[i][0])
        return headlist


    def handleChildAddButton(self, form):
        form.show()
        self.buttonbox.close()

    @LibMS
    def deleteRow(self, cursor, query):
        cursor.execute(query)

    @LibMS
    def getColumnNameList(self, cursor , tablename):
        cursor.execute("SHOW COLUMNS FROM "+tablename)
        data = cursor.fetchall()
        headlist = []
        for i in range(len(data)):
            headlist.append(data[i][0])
        return headlist

    def handleDeleteButton(self, cursor):
        index = self.papa.tabWidget.currentIndex()
        tabWidget = self.papa.tabWidget.widget(index).layout.itemAt(0).widget()
        selectedRows = [idx.row() for idx in tabWidget.selectionModel().selectedRows()]
        self.dialog = QMessageBox(self)
        self.dialog.setIcon(QMessageBox.Warning)
        if len(selectedRows) != 0:
            self.dialog.setText("These Rows will be deleted "+','.join([str(f+1) for f in selectedRows])+ " from table '"+self.papa.tabnames[index]+"'"+" \nAre You Sure?")
            self.dialog.setStandardButtons( QMessageBox.Yes | QMessageBox.No)
        else:
            self.dialog.setText("No Row was selected. Please select rows.")
            self.dialog.setStandardButtons( QMessageBox.Ok)

        self.dialog.setWindowTitle("Deletion")

        retval = self.dialog.exec_()
        if retval == QMessageBox.No or retval == QMessageBox.Ok:
            self.dialog.close()
            return
        self.dialog.close()

        try:
            for i in range(len(selectedRows)):
                q = "DELETE FROM "+self.papa.tabnames[index]+" WHERE"
                headlist = self.getColumnNameList(tablename=self.papa.tabnames[index])

                for j in range(len(headlist)):
                    if ("date" in headlist[j]) or ("time" in headlist[j]) or ("usertype" in headlist[j]):
                        continue

                    if "id" in headlist[j]:
                        q += " ("+headlist[j]+" = "+tabWidget.item(selectedRows[i],j).text()+" )"
                    elif "'" not in tabWidget.item(selectedRows[i],j).text():
                        q += " ("+headlist[j]+" = '"+tabWidget.item(selectedRows[i],j).text()+"' )"
                    else:
                        q += " ("+headlist[j]+' = "'+tabWidget.item(selectedRows[i],j).text()+'" )'

                    q += " AND"
                q = q[:-3]
                print(q)
                self.deleteRow(query=q)

            self.papa.tabWidget.refresh()
            self.dialog2 = QMessageBox(self)
            self.dialog2.setIcon(QMessageBox.Information)
            self.dialog2.setText("Successfully Deleted!")
            self.dialog2.setWindowTitle("Success!")
            self.dialog2.setStandardButtons(QMessageBox.Ok)
            self.dialog2.buttonClicked.connect(self.dialog2.close)
            self.dialog2.show()
        except:
            self.dialog2 = QMessageBox(self)
            self.dialog2.setIcon(QMessageBox.Critical)
            self.dialog2.setText("Most Probably. Foreign Key Constraint have Failed!. Try Again!")
            self.dialog2.setWindowTitle("Wrong Query!")
            self.dialog2.setStandardButtons(QMessageBox.Close)
            self.dialog2.buttonClicked.connect(self.dialog2.close)
            self.dialog2.show()

class SearchedWindow(QMainWindow):
    def __init__(self, parent, searchtext):
        super(SearchedWindow, self).__init__(parent)
        self.setWindowTitle("Search Output")
        self.tabnames = parent.tabnames
        
        queries = []
        for i in range(len(self.tabnames)):
            collist = self.getColumnNameList(tablename=self.tabnames[i])
            q = "SELECT * FROM "+self.tabnames[i]+" WHERE ("
            for j in range(len(collist)):
                q += collist[j]+" LIKE '%"+searchtext+"%')"
                if j+1 < len(collist):
                    q += " OR ("
            queries.append(q)

        self.tabWidget = TabWidget(self, queries)
        self.setCentralWidget(self.tabWidget)

    @LibMS
    def getColumnNameList(self, cursor , tablename):
        cursor.execute("SHOW COLUMNS FROM "+tablename)
        data = cursor.fetchall()
        headlist = []
        for i in range(len(data)):
            headlist.append(data[i][0])

        return headlist