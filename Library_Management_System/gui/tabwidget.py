from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from Library_Management_System.helper.helper import *
from functools import partial
import sys
import pymysql as sql

from Library_Management_System.gui.tablewidget import TableWidget

class TabWidget(QTabWidget):
    def __init__(self, parent, queries=None, tabnames=None):
        super(TabWidget, self).__init__(parent)
        self.tabnames = parent.tabnames
        self.tablist = []
        self.queries = queries
        self.papa = parent

        for i in range(len(self.tabnames)):
            self.tablist.append(QWidget())
            if(tabnames != None):
                self.addTab(self.tablist[i], tabnames[i])
            else:
                self.addTab(self.tablist[i], self.tabnames[i])

            self.tablist[i].layout = QVBoxLayout(self)
            if queries == None:
                self.tablist[i].layout.addWidget(TableWidget(self, tablename=self.tabnames[i]))
            else:
                self.tablist[i].layout.addWidget(TableWidget(self, tablename=self.tabnames[i], query=queries[i]))
            self.tablist[i].setLayout(self.tablist[i].layout)

    def refresh(self):
        for i in range(len(self.tablist)):
            # index = self.currentIndex()
            widget = self.widget(i).layout.itemAt(0).widget()
            widget.clear()
            widget.fillData(query=self.queries)
