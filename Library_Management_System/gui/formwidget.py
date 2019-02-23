from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from Library_Management_System.helper.helper import *
from functools import partial
import sys
import pymysql as sql


class FormDialog(QDialog):
    def __init__(self, parent, inputnamelist, tablename=None):
        super(FormDialog, self).__init__(parent)
        self.layout = QFormLayout(self)
        self.labels = []
        self.inputs = []
        self.papa = parent
        self.inputnamelist = inputnamelist
        self.tablename = tablename

        for i in range(len(inputnamelist)):
            tlabel = QLabel(inputnamelist[i])
            if inputnamelist[i] == "usertype":
                tinput = QComboBox(self)
                tinput.addItem("Faculty")
                tinput.addItem("Guest")
                tinput.addItem("Students")
                tinput.addItem("Staff")
            elif ("issuetime" in self.inputnamelist[i]) or ("datetime" in self.inputnamelist[i]) or ("timestamp" in self.inputnamelist[i]):
                tinput = QDateTimeEdit(self)
                tinput.setCalendarPopup(True)
                tinput.setDisplayFormat("dd-MM-yyyy hh:mm")
            elif "date" in self.inputnamelist[i]:
                tinput = QDateEdit(self)
                tinput.setCalendarPopup(True)
                tinput.setDisplayFormat("dd-MM-yyyy")
            else:
                tinput = QLineEdit(parent)
            
            self.labels.append(tlabel)
            self.inputs.append(tinput)
            if "id" in self.inputnamelist[i] or "pages" in self.inputnamelist[i]:
                reg = QRegExp("[0-9]+")
            elif "time" in self.inputnamelist[i]:
                reg = QRegExp("^([0-9]|0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$")
            elif "year" in self.inputnamelist[i]:
                reg = QRegExp("[0-9]{,4}")
            elif "name" in self.inputnamelist[i] or "title" in self.inputnamelist[i]:
                reg = QRegExp("[\s\S]+")
            else:
                reg = QRegExp("[\S]+")

            if type(self.inputs[i]) != QDateEdit and type(self.inputs[i]) != QDateTimeEdit:
                input_validator = QRegExpValidator(reg, self.inputs[i])
                self.inputs[i].setValidator(input_validator)            
            self.layout.addRow(tlabel, tinput)

        self.submitbtn = QPushButton("Submit")
        self.cancelbtn = QPushButton("Cancel")
        self.cancelbtn.clicked.connect(self.close)
        self.submitbtn.clicked.connect(lambda: self.addDatatoDatabase())
        self.labels.append(self.submitbtn)
        self.inputs.append(self.cancelbtn)
        self.layout.addRow(self.submitbtn, self.cancelbtn)

        self.setLayout(self.layout)

    @LibMS
    def addDatatoDatabase(self, cursor):
        query = "INSERT INTO "+self.tablename+" ("
        for i in range(len(self.inputnamelist)):
            query += " "+self.inputnamelist[i]+","
        query = query[:-1]
        query += ") VALUES ("
        for i in range(len(self.inputnamelist)):
            if type(self.inputs[i]) == QDateEdit :
                    query += " '"+self.inputs[i].date().toString("yyyy-MM-dd")+"',"
            elif type(self.inputs[i]) == QDateTimeEdit :
                    query += " '"+self.inputs[i].dateTime().toString("yyyy-MM-dd hh:mm:ss")+"',"
            elif type(self.inputs[i]) == QComboBox :
                    query += ' "'+self.inputs[i].currentText()+'",'
            elif(self.inputs[i].text() != ""):
                if "id" in self.inputnamelist[i] or "pages" in self.inputnamelist[i]:
                    query += " "+self.inputs[i].text()+","
                elif "'" in self.inputnamelist[i]:
                    query += ' "'+self.inputs[i].text()+'",'
                elif "time" in self.inputnamelist[i]:
                    query += " '"+self.inputs[i].text()+"',"
                elif "year" in self.inputnamelist[i]:
                    query += " '"+self.inputs[i].text()+"',"
                else:
                    query += ' "'+self.inputs[i].text()+'",'
            else:
                for j in range(len(self.inputnamelist)):
                    if type(self.inputs[j]) != QComboBox and type(self.inputs[j]) != QDateEdit and type(self.inputs[j]) != QDateTimeEdit:
                        self.inputs[j].clear()
                return
        query = query[:-1]
        query += " )"

        try:
            print(query)
            self.runQuery(quer=query)
        except:
            self.dialog2 = QMessageBox(self)
            self.dialog2.setIcon(QMessageBox.Critical)
            self.dialog2.setText("Can't Add. Incorrect Input. Try Again!")
            self.dialog2.setWindowTitle("Error!")
            self.dialog2.setStandardButtons(QMessageBox.Close)
            self.dialog2.buttonClicked.connect(self.dialog2.close)
            self.dialog2.show()
        self.papa.papa.tabWidget.refresh()
        self.close()

    @LibMS
    def runQuery(self, cursor, quer):
        cursor.execute(quer)