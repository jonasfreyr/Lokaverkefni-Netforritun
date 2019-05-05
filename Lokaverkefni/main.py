from PyQt5 import QtCore, QtGui, QtWidgets, sip
import socket, _thread, sys, os, time, datetime, site, threading
from profile import Ui_Profile
import base64
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\jonas\Desktop\test.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

print(os.path.dirname(sys.executable))
print(site.getsitepackages())

class Ui_MainWindow(object):
    def setupUi(self, MainWindow, start):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(528, 407)
        MainWindow.setIconSize(QtCore.QSize(24, 24))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(130, 340, 211, 21))
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
        self.servers.setGeometry(QtCore.QRect(440, 130, 71, 201))
        self.servers.setObjectName("servers")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 10, 121, 20))
        self.label.setObjectName("label")
        self.nameInput = QtWidgets.QLineEdit(self.centralwidget)
        self.nameInput.setGeometry(QtCore.QRect(10, 40, 111, 21))
        self.nameInput.setText("")
        self.nameInput.setObjectName("nameInput")
        self.textEdit = QtWidgets.QTextBrowser(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(130, 40, 301, 291))
        self.textEdit.setOpenExternalLinks(True)
        self.textEdit.setObjectName("textEdit")
        self.lobby_name = QtWidgets.QLabel(self.centralwidget)
        self.lobby_name.setGeometry(QtCore.QRect(130, 10, 301, 21))
        self.lobby_name.setText("")
        self.lobby_name.setAlignment(QtCore.Qt.AlignCenter)
        self.lobby_name.setObjectName("lobby_name")
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
        self.changeButton.clicked.connect(self.open_profile)
        self.servers.itemActivated.connect(self.select_lobby)
        self.online.itemActivated.connect(self.get_online_profile)

        self.name = "unkown_user"
        self.imgName = ""

        self.name_list = []
        self.prev = None
        self.lobbies = []

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
        self.connection.connect((start.ip, start.port))
        self.connection.sendall(self.name.encode())
        self.lobby = self.connection.recv(1024).decode()
        self.lobbies = eval(self.connection.recv(1024).decode())
        self.name_list = eval(self.connection.recv(1024).decode())

        self.set_lobby_name(self.lobby)

        for a in self.lobbies:
            self.add_lobby(a)

        for a in self.name_list:
            self.add_user(a)


        # _thread.start_new_thread(self.receive_data, ())
        self.thread = threading.Thread(target=self.receive_data, args=())
        self.thread.start()

        # QtCore.QObject.destroyed.connect(lambda: self.closeEvent())
        #app = QtWidgets.QApplication(sys.argv)

        self.send("::date")

    def get_online_profile(self, u):
        user = u.text()

        self.connection.sendall(str(["gu", user]).encode())

    def open_profile(self, online=False):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_Profile()

        if not online:
            self.ui.setupUi(self.window, False, self)

        else:
            self.ui.setupUi(self.window, True)

        self.window.show()

    def add_user(self, u):
        self.online.addItem(u)

    def remove_user(self, u):
        self.online.clear()
        self.name_list.remove(u)
        for a in self.name_list:
            self.add_user(a)

    def change_user(self, prev, now):
        self.remove_user(prev)

        self.name_list.append(now)

        self.add_user(now)


    def add_lobby(self, l):
        self.servers.addItem(l)

    def select_lobby(self, l):
        try:
            if self.lobby != l.text():
                self.lobby = l.text()
                self.connection.sendall(str(["cl", self.name, self.lobby]).encode())
                self.online.clear()
                self.set_lobby_name(self.lobby)
                self.send("::clear")
        except:
            self.lobby = l
            self.connection.sendall(str(["cl", self.name, self.lobby]).encode())
            self.online.clear()
            self.set_lobby_name(self.lobby)
            self.send("::clear")

    def set_lobby_name(self, n):
        self.lobby_name.setText(n)

    def receive_data(self):
        while True:
            try:
                data = eval(self.connection.recv(100000000).decode("utf-8"))
                # print(self.name_list)
                if data[0] == "c":
                    self.name_list.append(data[1])
                    self.add_user(data[1])
                    self.show_in_text(data[1] + "->" + "Connected",noName=True)

                elif data[0] == "m":
                    self.show_in_text(data[2], data[1])

                elif data[0] == "dc":
                    self.remove_user(data[1])
                    self.show_in_text(data[1] + "->" + "Disconnected",noName=True)

                elif data[0] == "cn":
                    self.change_user(data[1], data[2])
                    self.show_in_text(data[1] + "->" + data[2], noName=True)

                elif data[0] == "du":
                    self.name_list = data[1]
                    for a in self.name_list:
                        self.add_user(a)

                elif data[0] == "gu":
                    self.get_user(data[1])

                elif data[0] == "su":
                    self.online_profile(data)

            except:
                break

    def online_profile(self, data):
        with open("temp_name.txt", "w") as r:
            r.write(data[2][0])
            r.write("temp_img.png")

        with open("temp_profile.txt", "w") as r:
            r.write(data[2][2])

        with open("temp_img.png", "wb") as r:
            img = data[2][1]
            img = base64.b64decode(img)
            r.write(img)

        self.open_profile(True)

    def get_user(self, n):
        msg = ["su", n, []]
        with open("profile.txt", "r") as r:
            p = r.read()

        with open("name.txt", "r") as r:
            name = r.readline()
            img = r.readline()

        with open(img, "rb") as r:
            str_img = base64.b64encode(r.read())

        msg[2].append(name)
        msg[2].append(str_img)
        msg[2].append(p)

        self.connection.sendall(str(msg).encode())


    def write_to_file(self):
        with open("name.txt", "w") as r:
            r.write(self.name)
            r.write("\n")
            r.write(self.imgName)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "PyChat"))
        self.sendButton.setText(_translate("MainWindow", "Send"))
        self.selectButton.setText(_translate("MainWindow", "Select"))
        self.changeButton.setText(_translate("MainWindow", "Profile"))
        self.label.setText(_translate("MainWindow", "unknown"))

    def set_img(self, filename):
        pixmap = QtGui.QPixmap(filename)
        pixmap = pixmap.scaled(self.img.width(), self.img.height(), QtCore.Qt.KeepAspectRatio)
        self.img.setPixmap(pixmap)
        self.img.setAlignment(QtCore.Qt.AlignCenter)

    def set_name(self, v):
        self.label.setText(v)

    def change_name(self, value=None):
        if value is None:
            value = self.nameInput.text()
            self.nameInput.clear()

        if value:
            self.connection.sendall(str(["cn", self.name, value]).encode())
            self.set_name(value)
            self.show_in_text(self.name + "->" + value, noName=True)
            self.name = value

        self.write_to_file()

    def show_in_text(self, v, n=None, noName=False):
        color = "grey"

        if n is None:
            n = self.name
            color = "#100b00"

        if v[:8] == "https://":
            v = '<a href="{}"> {} </a>'.format(v, v)

        if not noName:
            n = '<span style="color:{}">{}</span>'.format(color, n)
            text = n + ": " + v

        elif noName:
            text = v

        self.textEdit.append(text)

        # self.textEdit.setText(self.text)
        time.sleep(0.01)
        s = self.textEdit.verticalScrollBar()
        s.setValue(s.maximum())

    def send_data(self, v):
        v = ["m", self.name, v]

        self.connection.sendall(str(v).encode())

    def send(self, value=None):
        if value is None or value is False:
            value = self.lineEdit.text()

            self.lineEdit.clear()

        if value[:2] == "::":
            if value[2:] == "clear":
                self.textEdit.clear()

            elif value[2:] == "date":
                now = datetime.datetime.now()
                self.show_in_text("Date" + "->" + now.strftime("%d-%m-%Y %H:%M:%S"), noName=True)

            elif value[2:] == "exit":
                quit()

            elif value[2:4] == "cn":
                value = value.split(" ", 1)
                self.change_name(value[1])

            elif value[2:4] == "cl":
                value = value.split(" ", 1)
                if value[1] in self.lobbies:
                    self.select_lobby(value[1])
            value = ""

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
