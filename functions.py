import re, os, ctypes, sys
from PyQt5.Qt import QIcon, QMenu, QSystemTrayIcon
from PyQt5.QtWidgets import QMessageBox
from PyQt5 import QtGui

emailCondition = "^[a-zA-Z]+[\._]?[a-zA-Z0-9]+[@]\w+[.]\w{2,}$"
emailCondition2 = r"[a-zA-Z\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+"
    
def getEmails(emails, flag=re.I):
    got_email = set(re.findall(emailCondition, emails, flag))
    if got_email == set():
        got_email = set(re.findall(emailCondition2, emails, flag))
    return got_email

def setTrayIconBackgroundWindow(app, window):
    app.setQuitOnLastWindowClosed(False)
    
    # Adding an icon    
    # Adding item on the menu bar
    tray = QSystemTrayIcon(QIcon("icons/clipboard-manager.ico"), parent=app)
    tray.setToolTip('Clipboard Manager')
    tray.show()
    
    # Creating the options
    menu = QMenu()    
    
    # To reopen the app
    open = menu.addAction('Open')
    open.triggered.connect(window.show)
    
    # To quit the app
    quit = menu.addAction('Quit')
    quit.triggered.connect(app.quit)
    
    # Adding options to the System Tray
    tray.setContextMenu(menu)

def MessageBox(windowIcon, mainIcon, text, title="Error"):
    font = QtGui.QFont()
    font.setFamily("MS Reference Sans Serif")
    font.setPointSize(10)
    msg = QMessageBox()
    msg.setFont(font)
    msg.setIcon(windowIcon)
    icon = QtGui.QIcon()
    icon.addPixmap(QtGui.QPixmap(mainIcon), QtGui.QIcon.Normal, QtGui.QIcon.Off)
    msg.setWindowIcon(icon)
    msg.setText(text)
    msg.setWindowTitle(title)
    msg.show()
    msg.exec_()