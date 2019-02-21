import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
 
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
        
        self.tabnames = ["Users", "Books", "Authors", "Papers", "History"]

        self.tabWidget = TabWidget(self)
        self.setCentralWidget(self.tabWidget) 
        self.show()
 

class TabWidget(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)

        self.tabnames = parent.tabnames        
        self.tabs = QTabWidget()
        self.tablist = []

        for i in range(len(self.tabnames)):
            self.tablist.append(QWidget())
            self.tabs.addTab(self.tablist[i],self.tabnames[i])
            self.tablist[i].layout = QVBoxLayout(self)
            self.tablist[i].layout.addWidget(TableWidget(self))
            self.tablist[i].setLayout(self.tablist[i].layout)

        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)


class TableWidget(QTableWidget):
    def __init__(self, parent):
        super(QTableWidget, self).__init__(parent)
        self.setColumnCount(10)
        self.setRowCount(10)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())