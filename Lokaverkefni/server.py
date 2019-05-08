import socket
import _thread
import time

HOST = "0.0.0.0"
PORT = 65432

nicks = {}

lobby_names = ["Lobby 1", "Lobby 2", "Lobby 3"]
lobby = {}
for a in lobby_names:
    lobby[a] = []

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Python\Lokaverkefni\server_window.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_server_window(object):
    def setupUi(self, server_window):
        server_window.setObjectName("server_window")
        server_window.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(server_window)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 10, 101, 31))
        font = QtGui.QFont()
        font.setPointSize(21)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(80, 70, 331, 481))
        self.textBrowser.setObjectName("textBrowser")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(180, 20, 101, 41))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(580, 30, 71, 21))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(480, 70, 256, 481))
        self.listWidget.setObjectName("listWidget")
        server_window.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(server_window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        server_window.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(server_window)
        self.statusbar.setObjectName("statusbar")
        server_window.setStatusBar(self.statusbar)

        self.retranslateUi(server_window)
        QtCore.QMetaObject.connectSlotsByName(server_window)

        _thread.start_new_thread(self.update_user, ())
        self.temp = nicks.copy()

    def retranslateUi(self, server_window):
        _translate = QtCore.QCoreApplication.translate
        server_window.setWindowTitle(_translate("server_window", "MainWindow"))
        self.label.setText(_translate("server_window", "Server"))
        self.label_2.setText(_translate("server_window", "Output"))
        self.label_3.setText(_translate("server_window", "Users"))

    def update_user(self):
        while True:
            if nicks != self.temp:
                print("yay")
                self.listWidget.clear()
                for nick in nicks:
                    self.listWidget.addItem(nicks[nick])

                self.temp = nicks.copy()

    def update_output(self, data):
        self.textBrowser.append(data)

def new_client(conn, addr):
    ui.update_output("Connection started with: " + str(addr))

    clobby = lobby_names[0]
    lobby[clobby].append(conn)

    conn.sendall(lobby_names[0].encode())
    conn.sendall(str(lobby_names).encode())

    msg = str(["c", nicks[conn]])
    for a in lobby[clobby]:
        if a != conn:
            a.sendall(msg.encode())

    users = []
    for a in lobby[clobby]:
        if a != conn:
            users.append(nicks[a])

    time.sleep(0.1)
    conn.sendall(str(users).encode())

    while True:
        try:
            send = True
            data = conn.recv(100000000)
            dataD = eval(data.decode())

            if dataD[0] == "cn":
                nicks[conn] = dataD[2]

            elif dataD[0] == "cl":
                msg = str(["dc", nicks[conn]]).encode()
                for a in lobby[clobby]:
                    if a != conn:
                        a.sendall(msg)

                lobby[clobby].remove(conn)
                clobby = dataD[2]

                users = []
                for a in lobby[clobby]:
                    if a != conn:
                        users.append(nicks[a])

                msg = ["du", users]
                conn.sendall(str(msg).encode())

                lobby[clobby].append(conn)

                msg = str(["c", nicks[conn]])
                for a in lobby[clobby]:
                    if a != conn:
                        a.sendall(msg.encode())

                send = False

            elif dataD[0] == "gu":
                for a in lobby[clobby]:
                    if nicks[a] == dataD[1]:
                        a.sendall(str(["gu", nicks[conn]]).encode())
                        break

                send = False

            elif dataD[0] == "su":
                for a in lobby[clobby]:
                    if nicks[a] == dataD[1]:
                        a.sendall(data)
                        break

                send = False

            elif dataD[0] == "ap":
                does_exist = False
                for a in nicks:
                    if dataD[1] == nicks[a]:
                        does_exist = True

                if does_exist:
                    conn.sendall(str(["ap", "no"]).encode())

                else:
                    conn.sendall(str(["ap", "yes"]).encode())

            ui.update_output(data.decode())

        except:
            ui.update_output("Connection ended with: " + str(addr))

            msg = str(["dc", nicks[conn]]).encode()
            for a in lobby[clobby]:
                if a != conn:
                    a.sendall(msg)

            lobby[clobby].remove(conn)
            del nicks[conn]
            break



        # ui.add_users(conn)
        if send == True:
            for a in lobby[clobby]:
                if a != conn:
                    a.sendall(data)


def socket_func():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()

        ui.update_output("Server started!")

        while True:
            conn, addr = s.accept()

            while True:
                nick = conn.recv(1024).decode("utf-8")
                does_exist = False
                for a in nicks:
                    if nick == nicks[a]:
                        does_exist = True
                        break

                if not does_exist:
                    conn.sendall(b"yes")
                    break

                else:
                    conn.sendall(b"no")



            nicks[conn] = nick

            _thread.start_new_thread(new_client, (conn, addr))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    server_window = QtWidgets.QMainWindow()
    ui = Ui_server_window()
    _thread.start_new_thread(socket_func, ())
    ui.setupUi(server_window)
    server_window.show()
    sys.exit(app.exec_())
