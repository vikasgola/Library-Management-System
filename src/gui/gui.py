from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets 
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
sys.path.append('../')
from helper.helper import *
from functools import partial

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = "Library Management System"
        self.left = 0
        self.top = 0
        self.width = 600
        self.height = 800
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        self.tabnames = ["User", "Book", "Author", "Paper", "Periodical", "Message", "Publisher", "History"]
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

class SearchedWindow(QMainWindow):
    def __init__(self, parent, searchtext):
        super(QMainWindow, self).__init__(parent)
        self.setWindowTitle("Search Output")
        self.tabnames = ["User", "Book", "Author", "Paper", "Periodical", "Message", "Publisher", "History"]
        
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


class QueryWindow(QMainWindow):
    def __init__(self, parent, query):
        super(QMainWindow, self).__init__(parent)
        self.setWindowTitle("Query Output")
        tableWidget = TableWidget(self, query=query)
        self.setCentralWidget(tableWidget)       

class TopbarWidget(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
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

    def closeDialog(self):
        self.dialog.close()
        self.searchBar.setText("")

    def handleSeachBar(self):
        if( ("SELECT" in self.searchBar.toPlainText()) or ("select" in self.searchBar.toPlainText()) ):
            queryWindow = QueryWindow(self.papa, self.searchBar.toPlainText())
            queryWindow.show()
        else:
            self.dialog = QMessageBox(self)
            self.dialog.setIcon(QMessageBox.Critical)
            self.dialog.setText("Not SELECT query!. Only SELECT queries can be used. Please Try Again with SELECT query.")
            self.dialog.setWindowTitle("Not SELECT query!")
            self.dialog.setStandardButtons(QMessageBox.Close)
            self.dialog.buttonClicked.connect(self.closeDialog)
            self.dialog.show()


class FormDialog(QDialog):
    def __init__(self, parent, inputnamelist):
        super(QDialog, self).__init__(parent)
        self.layout = QFormLayout(self)
        self.labels = []
        self.inputs = []
        for i in range(len(inputnamelist)):
            tlabel = QLabel(inputnamelist[i])
            tinput = QLineEdit(parent)
            self.labels.append(tlabel)
            self.inputs.append(tinput)
            self.layout.addRow(tlabel, tinput)

        self.submit = QPushButton("Submit")
        self.cancel = QPushButton("Cancel")
        self.cancel.clicked.connect(lambda: self.close())
        self.labels.append(self.submit)
        self.inputs.append(self.cancel)
        self.layout.addRow(self.submit, self.cancel)

        self.setLayout(self.layout)

class BottombarWidget(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QHBoxLayout(self)
        self.addSearchBar(parent)
        self.papa = parent

        self.btn1 = QPushButton(self)
        self.btn1.setText("Add Data")
        self.btn1.setFixedWidth(100)
        self.btn1.clicked.connect(self.handleAddButton)
        self.layout.addWidget(self.btn1, 1, Qt.AlignRight)
        
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

    def handleAddButton(self):
        self.buttonbox = QDialog(self)
        self.buttonbox.setFixedWidth(120)
        self.layout = QVBoxLayout(self.buttonbox)

        userbtn = QPushButton(self.buttonbox)
        userbtn.setText("Add User")
        inputfield = ["Name", "username", "password", "email", "usertype"]
        self.userform = FormDialog(self.buttonbox, inputfield)
        self.userform.setWindowTitle("Add new User")
        userbtn.clicked.connect(lambda: (self.userform.show(), self.buttonbox.close()))
        self.layout.addWidget(userbtn)

        bookbtn = QPushButton(self.buttonbox)
        bookbtn.setText("Add Book")
        inputfield = ["Title", "Pages", "Year", "isbn", "addDate", "Publisher Name"]
        self.bookform = FormDialog(self.buttonbox, inputfield)
        self.bookform.setWindowTitle("Add new Book")
        bookbtn.clicked.connect(lambda: (self.bookform.show(), self.buttonbox.close()))
        self.layout.addWidget(bookbtn)

        authorbtn = QPushButton(self.buttonbox)
        authorbtn.setText("Add Author")
        inputfield = ["Name"]
        self.authorform = FormDialog(self.buttonbox, inputfield)
        self.authorform.setWindowTitle("Add new Author")
        authorbtn.clicked.connect(lambda: (self.authorform.show(), self.buttonbox.close()))
        self.layout.addWidget(authorbtn)

        paperbtn = QPushButton(self.buttonbox)
        paperbtn.setText("Add Paper")
        inputfield = []
        self.paperform = FormDialog(self.buttonbox, inputfield)
        self.paperform.setWindowTitle("Add new Paper")
        paperbtn.clicked.connect(lambda: (self.paperform.show(), self.buttonbox.close()))
        self.layout.addWidget(paperbtn)

        messagebtn = QPushButton(self.buttonbox)
        messagebtn.setText("Add Message")
        inputfield = ["text", "timestamp", "user_id"]
        self.messageform = FormDialog(self.buttonbox, inputfield)
        self.messageform.setWindowTitle("Add new Message")
        messagebtn.clicked.connect(lambda: (self.messageform.show(), self.buttonbox.close()))
        self.layout.addWidget(messagebtn)

        publisherbtn = QPushButton(self.buttonbox)
        publisherbtn.setText("Add Pulisher")
        inputfield = ["Name"]
        self.publisherform = FormDialog(self.buttonbox, inputfield)
        self.publisherform.setWindowTitle("Add new Publisher")
        publisherbtn.clicked.connect(lambda: (self.publisherform.show(), self.buttonbox.close()))
        self.layout.addWidget(publisherbtn)

        cancelbtn = QPushButton(self.buttonbox)
        cancelbtn.setText("Cancel")
        cancelbtn.clicked.connect(lambda: self.buttonbox.close())
        self.layout.addWidget(cancelbtn)

        self.buttonbox.setLayout(self.layout)
        self.buttonbox.show()


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
                    if ("date" in headlist[j]) or ("time" in headlist[j]):
                        continue

                    if "id" in headlist[j]:
                        q += " ("+headlist[j]+" = "+tabWidget.item(selectedRows[i],j).text()+" )"
                    elif "'" not in tabWidget.item(selectedRows[i],j).text():
                        q += " ("+headlist[j]+" = '"+tabWidget.item(selectedRows[i],j).text()+"' )"
                    else:
                        q += " ("+headlist[j]+' = "'+tabWidget.item(selectedRows[i],j).text()+'" )'

                    q += " OR"
                q = q[:-2]
                self.deleteRow(query=q)
        except:
            self.dialog2 = QMessageBox(self)
            self.dialog2.setIcon(QMessageBox.Critical)
            self.dialog2.setText("Most Probably. Foreign Key Constraint have Failed!. Try Again!")
            self.dialog2.setWindowTitle("Wrong Query!")
            self.dialog2.setStandardButtons(QMessageBox.Close)
            self.dialog2.buttonClicked.connect(self.closeDialog)
            self.dialog2.show()
        self.papa.tabWidget.refresh()

    def closeDialog(self):
        self.dialog2.close()

class TabWidget(QTabWidget):
    def __init__(self, parent, queries=None):
        super(QTabWidget, self).__init__(parent)
        self.tabnames = parent.tabnames
        self.tablist = []

        for i in range(len(self.tabnames)):
            self.tablist.append(QWidget())
            self.addTab(self.tablist[i], self.tabnames[i])
            self.tablist[i].layout = QVBoxLayout(self)
            if queries == None:
                self.tablist[i].layout.addWidget(TableWidget(self, tablename=self.tabnames[i]))
            else:
                self.tablist[i].layout.addWidget(TableWidget(self, tablename=self.tabnames[i], query=queries[i]))
            self.tablist[i].setLayout(self.tablist[i].layout)

    def refresh(self):
        index = self.currentIndex()
        widget = self.widget(index).layout.itemAt(0).widget()
        widget.clear()
        widget.fillData()


class TableWidget(QtWidgets.QTableWidget):
    def __init__(self, parent, tablename=None, query=None):
        super(QtWidgets.QTableWidget, self).__init__(parent)
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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())