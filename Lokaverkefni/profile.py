# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\jonas\Desktop\Lokaverkefni-Netforritun-master\Lokaverkefni\profile.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
# from main import Ui_MainWindow

class Ui_Profile(object):
    def setupUi(self, Profile, Mainwindow=None):
        Profile.setObjectName("Profile")
        Profile.resize(325, 305)
        self.centralwidget = QtWidgets.QWidget(Profile)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(240, 10, 71, 61))
        self.label.setFrameShape(QtWidgets.QFrame.Box)
        self.label.setText("")
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(240, 80, 75, 23))
        self.pushButton.setObjectName("pushButton")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(10, 30, 221, 231))
        self.textEdit.setObjectName("textEdit")
        self.nameLabel = QtWidgets.QLabel(self.centralwidget)
        self.nameLabel.setGeometry(QtCore.QRect(10, 0, 221, 20))
        self.nameLabel.setText("")
        self.nameLabel.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse)
        self.nameLabel.setObjectName("nameLabel")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(240, 240, 75, 23))
        self.pushButton_2.setObjectName("pushButton_2")
        Profile.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(Profile)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 325, 21))
        self.menubar.setObjectName("menubar")
        Profile.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(Profile)
        self.statusbar.setObjectName("statusbar")
        Profile.setStatusBar(self.statusbar)

        self.retranslateUi(Profile)
        QtCore.QMetaObject.connectSlotsByName(Profile)

        self.pushButton.clicked.connect(self.change_img)
        self.pushButton_2.clicked.connect(self.save_profile)

        self.name = "unkown_user"
        self.imgName = ""

        self.profileText = ""

        self.Mainwindow = Mainwindow

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

        try:
            with open("profile.txt", "r") as r:
                self.profileText = r.read()

        except:
            with open("profile.txt", "x") as r:
                pass

        self.textEdit.setText(self.profileText)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "PyChat"))
        self.pushButton.setText(_translate("MainWindow", "Change"))
        self.pushButton_2.setText(_translate("MainWindow", "Save"))

    def save_profile(self):
        self.profileText = self.textEdit.toPlainText()
        with open("profile.txt", "w") as r:
            r.write(self.profileText)

        self.Mainwindow.imgName = self.imgName
        self.Mainwindow.set_img(self.imgName)

    def set_name(self, v):
        self.nameLabel.setText(v)

    def write_to_file(self):
        with open("name.txt", "w") as r:
            r.write(self.name)
            r.write("\n")
            r.write(self.imgName)

    def set_img(self, filename):
        pixmap = QtGui.QPixmap(filename)
        pixmap = pixmap.scaled(self.label.width(), self.label.height(), QtCore.Qt.KeepAspectRatio)
        self.label.setPixmap(pixmap)
        self.label.setAlignment(QtCore.Qt.AlignCenter)

    def change_img(self):
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(None, "Select image", "",
                                                            "image Files (*.png *.jpg *.jpeg *.bmp)")
        self.imgName = filename

        if filename:
            self.set_img(filename)

        self.write_to_file()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Profile = QtWidgets.QMainWindow()
    ui = Ui_Profile()
    ui.setupUi(Profile)
    Profile.show()
    sys.exit(app.exec_())

