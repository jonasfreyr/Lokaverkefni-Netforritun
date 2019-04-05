from PyQt5 import QtCore, QtGui, QtWidgets
import socket, _thread, atexit, sys, os

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\jonas\Desktop\test.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

HOST = "127.0.0.1"
PORT = 65432

print(os.path.dirname(sys.executable))


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
        self.textEdit.setEnabled(True)
        self.textEdit.setGeometry(QtCore.QRect(130, 40, 301, 291))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.textEdit.setFont(font)
        self.textEdit.setInputMethodHints(QtCore.Qt.ImhMultiLine)
        self.textEdit.setReadOnly(True)
        self.textEdit.setObjectName("textEdit")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 10, 121, 20))
        self.label.setObjectName("label")
        self.nameInput = QtWidgets.QLineEdit(self.centralwidget)
        self.nameInput.setGeometry(QtCore.QRect(10, 40, 111, 21))
        self.nameInput.setText("")
        self.nameInput.setObjectName("nameInput")
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

        self.lineEdit.returnPressed.connect(self.send)
        self.nameInput.returnPressed.connect(self.change_name)

        self.sendButton.clicked.connect(self.send)
        self.changeButton.clicked.connect(self.change_img)

        self.name = "unkown_user"
        self.imgName = ""

        self.name_list = []
        self.prev = None

        try:
            with open("name.txt", "r") as r:
                n = r.readline()
                n = n[:len(n) - 1]
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
        self.name_list = eval(self.connection.recv(1024).decode())
        for a in self.name_list:
            self.add_user(a)
        atexit.register(self.closes)

        _thread.start_new_thread(self.receive_data, ())

    def closes(self):
        print("closed!")
        self.connection.close()

    def add_user(self, u):
        self.online.addItem(u)

    def remove_user(self, u):
        self.online.clear()
        self.name_list.remove(u)
        for a in self.name_list:
            print(a)
            self.add_user(a)

    def change_user(self, prev, now):
        self.remove_user(prev)

        self.name_list.append(now)

        self.add_user(now)

    def receive_data(self):
        while True:
            try:
                data = eval(self.connection.recv(1024).decode("utf-8"))
                # print(self.name_list)
                if data[0] == "c":
                    self.name_list.append(data[1])
                    self.add_user(data[1])

                elif data[0] == "m":
                    self.show_in_text(data[2], data[1])
                    pass

                elif data[0] == "dc":
                    self.remove_user(data[1])

                elif data[0] == "cn":
                    self.change_user(data[1], data[2])
                    pass

            except:
                break

    def write_to_file(self):
        with open("name.txt", "w") as r:
            r.write(self.name)
            r.write("\n")
            r.write(self.imgName)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.sendButton.setText(_translate("MainWindow", "Send"))
        self.selectButton.setText(_translate("MainWindow", "Select"))
        self.changeButton.setText(_translate("MainWindow", "Change"))
        self.label.setText(_translate("MainWindow", "unknown"))

    def set_img(self, filename):
        pixmap = QtGui.QPixmap(filename)
        pixmap = pixmap.scaled(self.img.width(), self.img.height(), QtCore.Qt.KeepAspectRatio)
        self.img.setPixmap(pixmap)
        self.img.setAlignment(QtCore.Qt.AlignCenter)

    def change_img(self):
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(None, "Select image", "",
                                                            "image Files (*.png *.jpg *.jpeg *.bmp)")
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
            self.connection.sendall(str(["cn", self.name, value]).encode())
            self.set_name(value)
            self.name = value

        self.write_to_file()

    def show_in_text(self, v, n=None):
        e = "   "
        e2 = ""
        if n is None:
            n = self.name
            e = ""

        if n != self.prev and self.prev is not None:
            e2 = "\n"
            self.prev = n

        if self.prev is None:
            self.prev = n

        text = e2 + e + n + ": " + v
        self.textEdit.append(text)
        # self.textEdit.setText(self.text)

        s = self.textEdit.verticalScrollBar()
        s.setValue(s.maximum())

    def send_data(self, v):
        v = ["m", self.name, v]

        self.connection.sendall(str(v).encode())

    def send(self):
        value = self.lineEdit.text()

        self.lineEdit.clear()

        if value:
            self.send_data(value)
            self.show_in_text(value)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
