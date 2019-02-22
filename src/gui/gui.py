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
        self.width = 300
        self.height = 200
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
    def __init__(self, parent):
        super(SearchedWindow, self).__init__(parent)

class TopbarWidget(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QHBoxLayout(self)

        self.searchBar = QLineEdit()
        model = QStringListModel()
        index = parent.tabWidget.currentIndex()
        words = parent.tabWidget.widget(index).layout.itemAt(0).widget().words
        model.setStringList(words)

        completer = QCompleter()
        completer.setModel(model)
        self.searchBar.setCompleter(completer)
        self.layout.addWidget(self.searchBar, 1, Qt.AlignRight)

        self.btn1 = QPushButton(self)
        self.btn1.setIcon(QIcon('search.png'))
        self.btn1.setIconSize(QSize(18,18))
        self.btn1.clicked.connect(self.handleSeachBar)
        self.layout.addWidget(self.btn1 , 0, Qt.AlignRight)

        self.setLayout(self.layout)

    def handleSeachBar(self):
        searchedWindow = SearchedWindow(self.parent())
        searchedWindow.show()

class BottombarWidget(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QHBoxLayout(self)

        self.btn1 = QPushButton(self)
        self.btn1.setText("Add Data")
        self.btn1.setFixedWidth(100)
        self.layout.addWidget(self.btn1, 1, Qt.AlignRight)
        
        self.btn2 = QPushButton(self)
        self.btn2.setText("Delete Data")
        self.btn2.setFixedWidth(100)
        self.layout.addWidget(self.btn2, 0, Qt.AlignRight)
        
        self.setLayout(self.layout)


class TabWidget(QTabWidget):
    def __init__(self, parent):
        super(QTabWidget, self).__init__(parent)
        self.tabnames = parent.tabnames        
        self.tablist = []

        for i in range(len(self.tabnames)):
            self.tablist.append(QWidget())
            self.addTab(self.tablist[i], self.tabnames[i])
            self.tablist[i].layout = QVBoxLayout(self)
            self.tablist[i].layout.addWidget(TableWidget(self, self.tabnames[i]))
            self.tablist[i].setLayout(self.tablist[i].layout)


class TableWidget(QtWidgets.QTableWidget):
    def __init__(self, parent, tablename):
        super(QtWidgets.QTableWidget, self).__init__(parent)
        self.tablename = tablename
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.horizontalHeader().setSortIndicatorShown(True)
        self.fillData()
    
    @LibMS
    def fillData(self, cursor):
        cursor.execute("SELECT * FROM "+self.tablename)
        data = cursor.fetchall()
        self.setColumnCount(len(data[0]))
        self.setRowCount(len(data))

        self.words = []
        for d in range(len(data)):
            for dd in range(len(data[d])):
                self.words.append(str(data[d][dd]))
                self.setItem(d, dd, QtWidgets.QTableWidgetItem(str(data[d][dd])))

        cursor.execute("SHOW COLUMNS FROM "+self.tablename)
        data = cursor.fetchall()
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