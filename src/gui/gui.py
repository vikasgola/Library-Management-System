from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets 
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
sys.path.append('../')
from helper.helper import *


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
        super(SearchedWindow, self).__init__(parent)
        self.setWindowTitle("Search Output")
        self.tabnames = ["User", "Book", "Author", "Paper", "Periodical", "Message", "Publisher", "History"]
        
        queries = []
        for i in range(len(self.tabnames)):
            collist = self.getColumnNameList(tablename=self.tabnames[i])
            q = "SELECT * FROM "+self.tabnames[i]+" WHERE "
            for j in range(len(collist)):
                q += collist[j]+" = '"+searchtext+"'"
                if j+1 < len(collist):
                    q += " OR "
            queries.append(q) 

        centralWidget = QWidget(self)

        self.layout = QGridLayout(self)
        self.tabWidget = TabWidget(self, queries)
        self.bottombarWidget = BottombarWidget(self)

        self.layout.addWidget(self.tabWidget, 0 , 0)
        self.layout.addWidget(self.bottombarWidget, 1 , 0)

        centralWidget.setLayout(self.layout)
        self.setCentralWidget(centralWidget)

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
        super(QueryWindow, self).__init__(parent)
        self.setWindowTitle("Query Output")
        tableWidget = TableWidget(self, query=query)
        self.setCentralWidget(tableWidget)       

class TopbarWidget(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QHBoxLayout(self)
        self.setFixedHeight(64)

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
        if( ("SELECT" in self.searchBar.toPlainText()) or ("select" in self.searchBar.toPlainText()) ):
            queryWindow = QueryWindow(self.parent(), self.searchBar.toPlainText())
            queryWindow.show()
        else:
            pass

class BottombarWidget(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QHBoxLayout(self)
        self.addSearchBar(parent)

        self.btn1 = QPushButton(self)
        self.btn1.setText("Add Data")
        self.btn1.setFixedWidth(100)
        self.layout.addWidget(self.btn1, 1, Qt.AlignRight)
        
        self.btn2 = QPushButton(self)
        self.btn2.setText("Delete Data")
        self.btn2.setFixedWidth(100)
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
        searchedWindow = SearchedWindow(self.parent(), searchtext)
        searchedWindow.show()


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
        pass


class TableWidget(QtWidgets.QTableWidget):
    def __init__(self, parent, tablename=None, query=None):
        super(QtWidgets.QTableWidget, self).__init__(parent)
        self.tablename = tablename
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.horizontalHeader().setSortIndicatorShown(True)
        if query == None and tablename != None:
            self.fillData()
        elif query != None and tablename != None:
            self.fillData(query=query)
        elif query != None and tablename == None:
            self.fillData(query=query)

    
    @LibMS
    def fillData(self, cursor, query=None):
        if query == None:
            cursor.execute("SELECT * FROM "+self.tablename)
        else:
            print(query)
            cursor.execute(query)
        data = cursor.fetchall()
        
        if(len(data) != 0):
            self.setColumnCount(len(data[0]))
            self.setRowCount(len(data))

            self.words = []
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
        # for currentQTableWidgetItem in self.selectedItems():
        #     print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())