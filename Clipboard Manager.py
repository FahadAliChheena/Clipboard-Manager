# -*- coding: utf-8 -*-

# Author: Fahad Ali
# Date:   7/29/2022
# Name:   ClipboardManager

from genericpath import exists
from PyQt5 import QtWidgets, uic, QtGui, QtCore
import sys, os
from PyQt5.QtWidgets import QMessageBox, QCheckBox
from PyQt5.Qt import QApplication
from functions import getEmails, setTrayIconBackgroundWindow as setAppOnTray, MessageBox
from urlextract import URLExtract
from about import Ui_Dialog
from datetime import datetime

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('clipboard-manager.ui', self)
        self.setFixedSize(400, 300)
        QApplication.clipboard().dataChanged.connect(self.getClipboardData)
        # File Menu
        self.actionNew.triggered.connect(self.newClipboard)
        self.actionEmail_Extractor.triggered.connect(self.emailExtractor)
        self.actionURL_Extractor.triggered.connect(self.urlExtractor)
        self.actionExit.triggered.connect(self.close)
        # History Menu
        self.actionCheck_History.triggered.connect(self.checkHistory)
        self.actionClear_History.triggered.connect(self.clearHistory)
        # Help Menu
        self.actionAbout.triggered.connect(self.about)
        
    def getClipboardData(self):
        text = QApplication.clipboard().text()
        date = datetime.today()
        date, __ = str(date).split(' ')
        date = "Dated: "+date
        saved = set()
        if not date in saved:
            saved.add(date)
        exists = os.path.isfile('ClipboardData.list')
        if exists:
            f = open('ClipboardData.list', 'r')
            for data in f.readlines():
                saved.add(data.strip())
            f.close()
        if (not text.strip(' \r\n') in saved):
            self.plainTextEdit.insertPlainText(text.strip(' \r\n')+'\n')
            saved.add(text.strip(' \r\n'))
        f = open('ClipboardData.list', 'w')
        for text in saved:
            f.write(text+'\n')
        f.close()
        
    def checkHistory(self):
        exists = os.path.isfile('ClipboardData.list')
        # saved = set()
        if exists:
            f = open('ClipboardData.list', 'r')
            for data in f.readlines():
                self.plainTextEdit.appendPlainText(data.strip())
            f.close()
            # for text in saved:
            #     self.plainTextEdit.setPlainText(text+'\n')
        else:
            MessageBox(QMessageBox.Warning, "icons/error.ico", "History is empty.")
            
    def clearHistory(self):
        exists = os.path.isfile('ClipboardData.list')
        self.plainTextEdit.clear()
        if exists:
            os.remove('ClipboardData.list')
            MessageBox(QMessageBox.Information, "icons/about.png" , "History is cleared.", "Information")
        else:
            MessageBox(QMessageBox.Information, "icons/about.png" , "History is already empty.", "Information")
            
    def newClipboard(self):
        self.plainTextEdit.clear()
        
    def emailExtractor(self):
        text = self.plainTextEdit.toPlainText()
        got_emails = getEmails(text.strip( ' \r\n'))
        if not got_emails == set():
            fname = QtWidgets.QFileDialog.getSaveFileName(self, 'Save file', 
            'c:\\',"Text files (*.txt)")
            f = open(fname[0], 'w')
            for email in got_emails:
                f.write(email+'\n')
            f.close()
            MessageBox(QMessageBox.Information, "icons/about.png" , "Emails extracted successfully!", "Successful")
        else:
            MessageBox(QMessageBox.Information, "icons/about.png" , "No email is found in the text.", "Information")
            
    def urlExtractor(self):
        text = self.plainTextEdit.toPlainText()
        extractor = URLExtract()
        got_urls = extractor.find_urls(text.strip( ' \r\n'))
        if not got_urls == set():
            fname = QtWidgets.QFileDialog.getSaveFileName(self, 'Save file', 
            'c:\\',"Text files (*.txt)")
            f = open(fname[0], 'w')
            for url in got_urls:
                f.write(url+'\n')
            f.close()
            MessageBox(QMessageBox.Information, "icons/about.png" , "URLs extracted successfully!", "Successful")
        else:
            MessageBox(QMessageBox.Information, "icons/about.png" , "No URL is found in the text.", "Successful")
            
    def about(self):
        self.about = QtWidgets.QDialog()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self.about)
        #self.searchWindow.setParent(window)
        self.about.show()
        
    def closeEvent(self, event):
        self.hide()
        exists = os.path.isfile('check.con')
        read = False
        data = []
        if exists:
            f = open('check.con', 'r')
            for line in f.readlines():
                data.append(line.strip())
            f.close()
        if len(data) != 0:
            if data[-1] == "Checked":
                read = True
        text = ("1) Application is running in the background\n2)To close it go to the window tray icon\n3) Right click on icon\n4) Click on exit.")
        # MessageBox(QMessageBox.Information, "icons/about.png" , text, "Information")
        if read == False:
            Message = QMessageBox()
            check = QCheckBox("Don't show this message again.")
            check.stateChanged.connect(self.clickBox)
            Message.setCheckBox(check)
            Message.setText(text)
            Message.setWindowTitle("Information")
            Message.setIcon(QMessageBox.Information)
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap("icons/about.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            Message.setWindowIcon(icon)
            Message.show()
            Message.exec_()
        
    def clickBox(self, state):
        exists = os.path.isfile('check.con')
        if exists:
            f = open('check.con', 'a')
        else:
            f = open('check.con', 'w')
        if state == QtCore.Qt.Checked:
            f.write("Checked"+'\n')
        else:
            f.write('Unchecked'+'\n')
        f.close()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    window.show()
    setAppOnTray(app=app, window=window)
    app.exec_()