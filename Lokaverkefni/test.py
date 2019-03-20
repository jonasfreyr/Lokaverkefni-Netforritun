from PyQt5 import QtCore, QtGui, QtWidgets
import socket, _thread, atexit
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\jonas\Desktop\test.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

HOST = "127.0.0.1"
PORT = 65432


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(528, 407)
        MainWindow.setIconSize(QtCore.QSize(24, 24))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(140, 340, 201, 21))
        self.lineEdit.setText("")
        self.lineEdit.setObjectName("lineEdit")
        self.sendButton = QtWidgets.QPushButton(self.centralwidget)
        self.sendButton.setGeometry(QtCore.QRect(350, 340, 75, 23))
        self.sendButton.setObjectName("sendButton")
        self.online = QtWidgets.QListWidget(self.centralwidget)
        self.online.setGeometry(QtCore.QRect(10, 70, 111, 291))
        self.online.setObjectName("online")
        self.selectButton = QtWidgets.QPushButton(self.centralwidget)
        self.selectButton.setGeometry(QtCore.QRect(440, 340, 75, 23))
        self.selectButton.setObjectName("selectButton")
        self.img = QtWidgets.QLabel(self.centralwidget)
        self.img.setGeometry(QtCore.QRect(440, 20, 71, 61))
        self.img.setFrameShape(QtWidgets.QFrame.Box)
        self.img.setText("")
        self.img.setObjectName("img")
        self.changeButton = QtWidgets.QPushButton(self.centralwidget)
        self.changeButton.setGeometry(QtCore.QRect(440, 90, 75, 23))
        self.changeButton.setObjectName("changeButton")
        self.servers = QtWidgets.QListWidget(self.centralwidget)
        self.servers.setGeometry(QtCore.QRect(440, 130, 71, 191))
        self.servers.setObjectName("servers")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(130, 40, 301, 291))
        self.textEdit.setObjectName("textEdit")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(90, 10, 121, 20))
        self.label.setObjectName("label")
        self.nameInput = QtWidgets.QLineEdit(self.centralwidget)
        self.nameInput.setGeometry(QtCore.QRect(10, 40, 111, 21))
        self.nameInput.setText("")
        self.nameInput.setObjectName("nameInput")
        self.nameButton = QtWidgets.QPushButton(self.centralwidget)
        self.nameButton.setGeometry(QtCore.QRect(10, 10, 71, 23))
        self.nameButton.setObjectName("nameButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 528, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.sendButton.clicked.connect(self.send)
        self.nameButton.clicked.connect(self.change_name)
        self.changeButton.clicked.connect(self.change_img)

        self.name = "unkown_user"
        self.imgName = ""

        self.text = ""

        try:
            with open("name.txt", "r") as r:
                n = r.readline()
                n = n[:len(n)-1]
                i = r.readline()

                if n:
                    self.name = n
                    try:
                        self.set_name(n)
                    except:
                        self.name = ""

                if i:
                    self.imgName = i
                    try:
                        self.set_img(i)
                    except:
                        self.imgName = ""

        except:
            with open("name.txt", "x") as r:
                pass

        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((HOST, PORT))
        self.connection.sendall(self.name.encode())
        atexit.register(self.closes)

        _thread.start_new_thread(self.receive_data, ())


    def closes(self):
        print("closed!")
        self.connection.close()

    def receive_data(self):
        while True:
            data = self.connection.recv(1024).decode("utf-8")
            print(data)
            # data = s.recv(1024).decode("utf-8")


    def write_to_file(self):
        with open("name.txt", "w") as r:
            r.write(self.name)
            r.write("\n")
            r.write(self.imgName)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Chat App"))
        self.sendButton.setText(_translate("MainWindow", "Send"))
        self.selectButton.setText(_translate("MainWindow", "Select"))
        self.changeButton.setText(_translate("MainWindow", "Change"))
        self.label.setText(_translate("MainWindow", "unknown_user"))
        self.nameButton.setText(_translate("MainWindow", "Name"))

    def set_img(self, filename):
        pixmap = QtGui.QPixmap(filename)
        pixmap = pixmap.scaled(self.img.width(), self.img.height(), QtCore.Qt.KeepAspectRatio)
        self.img.setPixmap(pixmap)
        self.img.setAlignment(QtCore.Qt.AlignCenter)

    def change_img(self):
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(None, "Select image", "", "image Files (*.png *.jpg *.jpeg *.bmp)")
        print(filename)
        self.imgName = filename

        if filename:
            self.set_img(filename)

        self.write_to_file()

    def set_name(self, v):
        self.label.setText(v)

    def change_name(self):
        value = self.nameInput.text()
        self.nameInput.clear()
        if value:
            self.set_name(value)
            self.name = value

        self.write_to_file()

    def show_in_text(self, v, n = None):
        if n is None:
            n = self.name

        self.text += n + ": " + v + "\n"
        self.textEdit.setText(self.text)

        s = self.textEdit.verticalScrollBar()
        s.setValue(s.maximum())

    def send(self):
        value = self.lineEdit.text()

        self.lineEdit.clear()

        if value:
            self.show_in_text(value)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

