from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from Library_Management_System.helper.helper import *
from functools import partial
import sys
import pymysql as sql


class FormDialog(QDialog):
    def __init__(self, parent, inputnamelist, tablename, update=False, dataToFill=None):
        super(FormDialog, self).__init__(parent)
        self.layout = QFormLayout(self)
        self.labels = []
        self.inputs = []
        self.papa = parent
        self.inputnamelist = inputnamelist
        self.tablename = tablename
        self.dataToFill = dataToFill

        for i in range(len(inputnamelist)):
            if (tablename == "Book" or tablename == "Periodical") and (inputnamelist[i] == "user_id" or inputnamelist[i] == "issuetime") :
                tlabel = QLabel(inputnamelist[i]+" (optional)")
            else:
                tlabel = QLabel(inputnamelist[i])
            
            if inputnamelist[i] == "usertype":
                tinput = QComboBox(self)
                tinput.addItem("Faculty")
                tinput.addItem("Guest")
                tinput.addItem("Students")
                tinput.addItem("Staff")
                if dataToFill != None:
                    tlist = ["Faculty", "Guest", "Students", "Staff"]
                    try:
                        tinput.setCurrentIndex(tlist.index(dataToFill[i]))
                    except:
                        pass
            elif ("issuetime" in self.inputnamelist[i]) or ("datetime" in self.inputnamelist[i]):
                tinput = QDateTimeEdit(self)
                tinput.setCalendarPopup(True)
                tinput.setDisplayFormat("dd-MM-yyyy hh:mm")
                if dataToFill != None:
                    tinput.setDateTime(QDateTime.fromString(dataToFill[i]))
            elif "date" in self.inputnamelist[i]:
                tinput = QDateEdit(self)
                tinput.setCalendarPopup(True)
                tinput.setDisplayFormat("dd-MM-yyyy")
                if dataToFill != None:
                    tinput.setDate(QDate.fromString(dataToFill[i]))
            elif "timestamp" in self.inputnamelist[i]:
                continue
            else:
                tinput = QLineEdit(parent)            
                if dataToFill != None:
                    if dataToFill[i] == "None" or dataToFill[i] == None:
                        pass
                    if "year" in self.inputnamelist[i]:
                        tinput.setText(dataToFill[i][2:])
                    else:
                        tinput.setText(dataToFill[i])
                    
            self.labels.append(tlabel)
            self.inputs.append(tinput)
            if "id" in self.inputnamelist[i] or "pages" in self.inputnamelist[i] or "volume" in self.inputnamelist[i]:
                reg = QRegExp("[0-9]+")
            elif "time" in self.inputnamelist[i]:
                reg = QRegExp("^([0-9]|0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$")
            elif "year" in self.inputnamelist[i]:
                reg = QRegExp("[0-9]{,2}")
            elif "name" in self.inputnamelist[i] or "title" in self.inputnamelist[i] or "text" in self.inputnamelist[i]:
                reg = QRegExp("[\s\S]+")
            else:
                reg = QRegExp("[\S]+")

            if type(self.inputs[i]) != QDateEdit and type(self.inputs[i]) != QDateTimeEdit:
                input_validator = QRegExpValidator(reg, self.inputs[i])
                self.inputs[i].setValidator(input_validator)            
            self.layout.addRow(tlabel, tinput)

        if not update:
            self.submitbtn = QPushButton("Submit")
        else:
            self.submitbtn = QPushButton("Update")

        self.cancelbtn = QPushButton("Cancel")
        self.cancelbtn.clicked.connect(self.close)
        try: self.submitbtn.clicked.disconnect() 
        except Exception: pass
        if not update:
            self.submitbtn.clicked.connect(self.addDatatoDatabase)
        else:
            self.submitbtn.clicked.connect(self.updateDatatoDatabase)

        self.labels.append(self.submitbtn)
        self.inputs.append(self.cancelbtn)
        self.layout.addRow(self.submitbtn, self.cancelbtn)

        self.setLayout(self.layout)


    def updateDatatoDatabase(self):
        uind = -1
        isUNull = False
        if self.tablename == "Book" or self.tablename == "Periodical":
            uind = self.inputnamelist.index("user_id")
            if self.inputs[uind].text() == "":
                self.inputs[uind].setText("NULL")
                isUNull = True

        query = "UPDATE "+self.tablename+" SET "
        
        for i in range(len(self.inputnamelist)):
            if type(self.inputs[i]) == QDateEdit :
                query += self.inputnamelist[i]+"='"+self.inputs[i].date().toString("yyyy-MM-dd")+"',"
            elif type(self.inputs[i]) == QDateTimeEdit :
                if isUNull:
                    query += self.inputnamelist[i]+"= NULL,"                
                else:
                    query += self.inputnamelist[i]+"='"+self.inputs[i].dateTime().toString("yyyy-MM-dd hh:mm:ss")+"',"
            elif type(self.inputs[i]) == QComboBox :
                query += self.inputnamelist[i]+"='"+self.inputs[i].currentText()+"',"
            elif(self.inputs[i].text() != ""):
                if "id" in self.inputnamelist[i] or "pages" in self.inputnamelist[i] or "volume" in self.inputnamelist[i]:
                    query += self.inputnamelist[i]+"= "+self.inputs[i].text()+","
                elif "timestamp" in self.inputnamelist[i]:
                    query += self.inputnamelist[i]+"='"+QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss")+"',"
                elif "time" in self.inputnamelist[i]:
                    query += self.inputnamelist[i]+"='"+self.inputs[i].text()+"',"
                elif "year" in self.inputnamelist[i]:
                    query += self.inputnamelist[i]+"='"+self.inputs[i].text()+"',"
                elif "'" in self.inputs[i].text():
                    query += self.inputnamelist[i]+'= "'+self.inputs[i].text()+'",'
                else:
                    query += self.inputnamelist[i]+"= '"+self.inputs[i].text()+"',"
            else:
                for j in range(len(self.inputnamelist)):
                    if type(self.inputs[j]) != QPushButton and type(self.inputs[j]) != QComboBox and type(self.inputs[j]) != QDateEdit and type(self.inputs[j]) != QDateTimeEdit:
                        self.inputs[j].clear()
                return
        query = query[:-1]
        query += " WHERE "

        headlist = self.inputnamelist
        for j in range(len(headlist)):
            if ("date" in headlist[j]) or ("time" in headlist[j]) or ("usertype" in headlist[j] or self.dataToFill[j] == "None" or self.dataToFill[j] == None):
                continue
            if "id" in headlist[j] or "pages" in headlist[j] or "volume" in headlist[j]:
                query += " ("+headlist[j]+" = "+self.dataToFill[j]+" )"
            elif "year" in self.dataToFill[j]:
                query += " ("+headlist[j]+" = '"+self.dataToFill[j][2:]+"' )"            
            elif "'" not in self.dataToFill[j]:
                query += " ("+headlist[j]+" = '"+self.dataToFill[j]+"' )"
            else:
                query += " ("+headlist[j]+' = "'+self.dataToFill[j]+'" )'

            query += " AND"
        query = query[:-3]

        try:
            print(query)
            self.runQuery(quer=query)
            self.papa.papa.tabWidget.refresh()
            self.dialog2 = QMessageBox(self)
            self.dialog2.setIcon(QMessageBox.Information)
            self.dialog2.setText("Successfully Updated!")
            self.dialog2.setWindowTitle("Success!")
            self.dialog2.setStandardButtons(QMessageBox.Ok)
            self.dialog2.buttonClicked.connect(self.dialog2.close)
            self.dialog2.show()
        except:
            self.dialog2 = QMessageBox(self)
            self.dialog2.setIcon(QMessageBox.Critical)
            self.dialog2.setText("Can't Update. Incorrect Input. Try Again!")
            self.dialog2.setWindowTitle("Error!")
            self.dialog2.setStandardButtons(QMessageBox.Close)
            self.dialog2.buttonClicked.connect(self.dialog2.close)
            self.dialog2.show()
        self.close()

    def addDatatoDatabase(self):
        uind = -1
        isUNull = False
        if self.tablename == "Book" or self.tablename == "Periodical":
            uind = self.inputnamelist.index("user_id")
            if self.inputs[uind].text() == "":
                self.inputs[uind].setText("NULL")
                isUNull = True

        query = "INSERT INTO "+self.tablename+" ("
        for i in range(len(self.inputnamelist)):
            query += " "+self.inputnamelist[i]+","
        query = query[:-1]
        query += ") VALUES ("
        for i in range(len(self.inputnamelist)):
            if type(self.inputs[i]) == QDateEdit :
                query += " '"+self.inputs[i].date().toString("yyyy-MM-dd")+"',"
            elif type(self.inputs[i]) == QDateTimeEdit :
                if isUNull:
                    query += " NULL,"
                else:
                    query += " '"+self.inputs[i].dateTime().toString("yyyy-MM-dd hh:mm:ss")+"',"
            elif type(self.inputs[i]) == QComboBox :
                query += ' "'+self.inputs[i].currentText()+'",'
            elif(self.inputs[i].text() != ""):
                if "id" in self.inputnamelist[i] or "pages" in self.inputnamelist[i] or "volume" in self.inputnamelist[i]:
                    query += " "+self.inputs[i].text()+","
                elif "'" in self.inputs[i].text():
                    query += ' "'+self.inputs[i].text()+'",'
                elif "timestamp" in self.inputnamelist[i]:
                    query += " '"+QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss")+"',"
                elif "time" in self.inputnamelist[i]:
                    query += " '"+self.inputs[i].text()+"',"
                elif "year" in self.inputnamelist[i]:
                    query += " '"+self.inputs[i].text()+"',"
                else:
                    query += " '"+self.inputs[i].text()+"',"
            else:
                for j in range(len(self.inputnamelist)):
                    if type(self.inputs[j]) != QPushButton and type(self.inputs[j]) != QComboBox and type(self.inputs[j]) != QDateEdit and type(self.inputs[j]) != QDateTimeEdit:
                        self.inputs[j].clear()
                return
        query = query[:-1]
        query += " )"

        try:
            print(query)
            self.runQuery(quer=query)
            self.papa.papa.tabWidget.refresh()
            self.dialog2 = QMessageBox(self)
            self.dialog2.setIcon(QMessageBox.Information)
            self.dialog2.setText("Successfully Added!")
            self.dialog2.setWindowTitle("Success!")
            self.dialog2.setStandardButtons(QMessageBox.Ok)
            self.dialog2.buttonClicked.connect(self.dialog2.close)
            self.dialog2.show()
        except:
            self.dialog2 = QMessageBox(self)
            self.dialog2.setIcon(QMessageBox.Critical)
            self.dialog2.setText("Can't Add. Incorrect Input. Try Again!")
            self.dialog2.setWindowTitle("Error!")
            self.dialog2.setStandardButtons(QMessageBox.Close)
            self.dialog2.buttonClicked.connect(self.dialog2.close)
            self.dialog2.show()
        self.close()

    @LibMS
    def runQuery(self, cursor, quer):
        cursor.execute(quer)