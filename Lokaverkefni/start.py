# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Python\Lokaverkefni\start.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from main import Ui_MainWindow

class Start_Window(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(466, 361)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.ipEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.ipEdit.setGeometry(QtCore.QRect(120, 110, 331, 31))
        self.ipEdit.setObjectName("ipEdit")
        self.portEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.portEdit.setGeometry(QtCore.QRect(120, 180, 331, 31))
        self.portEdit.setObjectName("portEdit")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 112, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(20, 180, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(160, 40, 131, 21))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(120, 240, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 466, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.ip = None
        self.port = None

        self.ipEdit.setText("127.0.0.1")
        self.portEdit.setText("65432")

        self.ipEdit.returnPressed.connect(self.connect)
        self.portEdit.returnPressed.connect(self.connect)
        self.pushButton.clicked.connect(self.connect)

    def connect(self):
        ip = self.ipEdit.text()
        port = self.portEdit.text()

        if ip and port:
            work = False
            try:
                port = int(port)
                work = True

            except:
                print("Port is not a number")

            if work:
                self.ip = ip
                self.port = port

                self.open()

    def open(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()

        self.ui.setupUi(self.window, self)
        MainWindow.hide()
        self.window.show()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "IP:"))
        self.label_2.setText(_translate("MainWindow", "Port:"))
        self.label_3.setText(_translate("MainWindow", "Pls Connect"))
        self.pushButton.setText(_translate("MainWindow", "Connect"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Start_Window()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

