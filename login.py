# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'login.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import uic, QtWidgets, QtCore, QtGui, QtPrintSupport
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QFileDialog, QApplication, QWidget, QErrorMessage, QTableWidgetItem, QLineEdit, QDialog, QMainWindow, QMessageBox
import sys

class Ui_login(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1152, 620)
        MainWindow.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        MainWindow.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setMinimumSize(QtCore.QSize(330, 400))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setGeometry(QtCore.QRect(0, 0, 341, 391))
        self.label.setStyleSheet("border-image: url(Logo sem circulo.png);\n"
"border-top-left-radius: 50px;")
        self.label.setText("")
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.frame, 0, QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
        self.frame_2 = QtWidgets.QFrame(self.centralwidget)
        self.frame_2.setMinimumSize(QtCore.QSize(250, 400))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.label_3 = QtWidgets.QLabel(self.frame_2)
        self.label_3.setGeometry(QtCore.QRect(80, 50, 81, 40))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("color:rgba(0, 0, 0, 200);\n"
"background-color: rgb(255, 255, 255);")
        self.label_3.setObjectName("label_3")
        self.senha = QtWidgets.QLineEdit(self.frame_2)
        self.senha.setGeometry(QtCore.QRect(10, 190, 201, 40))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.senha.setFont(font)
        self.senha.setStyleSheet("background-color:rgba(0, 0, 0, 0);\n"
"border:none;\n"
"border-bottom:2px solid rgba(0, 0, 0, 240);\n"
"color:rgba(0, 0, 0, 240);\n"
"padding-bottom:7px;\n"
"")
        self.senha.setEchoMode(QtWidgets.QLineEdit.Password)
        self.senha.setAlignment(QtCore.Qt.AlignCenter)
        self.senha.setDragEnabled(False)
        self.senha.setObjectName("senha")
        self.usuario = QtWidgets.QLineEdit(self.frame_2)
        self.usuario.setGeometry(QtCore.QRect(10, 120, 201, 40))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.usuario.setFont(font)
        self.usuario.setStyleSheet("background-color:rgba(0, 0, 0, 0);\n"
"border:none;\n"
"border-bottom:2px solid rgba(0, 0, 0, 240);\n"
"color:rgba(0, 0, 0, 240);\n"
"padding-bottom:7px;\n"
"")
        self.usuario.setAlignment(QtCore.Qt.AlignCenter)
        self.usuario.setObjectName("usuario")
        self.label_2 = QtWidgets.QLabel(self.frame_2)
        self.label_2.setGeometry(QtCore.QRect(0, 0, 251, 391))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"border-bottom-right-radius: 50px;")
        self.label_2.setText("")
        self.label_2.setObjectName("label_2")
        self.bt_vsenha = QtWidgets.QPushButton(self.frame_2)
        self.bt_vsenha.setGeometry(QtCore.QRect(190, 200, 21, 21))
        self.bt_vsenha.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.bt_vsenha.setStyleSheet("border-radius: 10px;\n"
"background-color: rgb(121, 121, 121);")
        self.bt_vsenha.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("Icones/mostrarsenha.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon.addPixmap(QtGui.QPixmap("Icones/ocultarsenha.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.bt_vsenha.setIcon(icon)
        self.bt_vsenha.setIconSize(QtCore.QSize(25, 25))
        self.bt_vsenha.setCheckable(True)
        self.bt_vsenha.setChecked(False)
        self.bt_vsenha.setAutoExclusive(False)
        self.bt_vsenha.setObjectName("bt_vsenha")
        self.bt_login = QtWidgets.QPushButton(self.frame_2)
        self.bt_login.setGeometry(QtCore.QRect(70, 250, 91, 31))
        self.bt_login.setStyleSheet("QPushButton#bt_login{\n"
"    background-color: rgb(0, 0, 0);\n"
"    border-radius:5px;\n"
"    color: rgb(255, 255, 255);\n"
"}\n"
"\n"
"QPushButton#bt_login:hover{\n"
"    background-color: rgb(254,117, 24);\n"
"    color: rgb(0, 0, 0);\n"
"}\n"
"\n"
"QPushButton#bt_login:pressed{\n"
"    padding-left:5px;\n"
"    padding-top:5px;\n"
"    background-color: rgb(0,0, 0);    \n"
"    color: rgb(255, 255, 255);\n"
"}")
        self.bt_login.setObjectName("bt_login")
        self.label_2.raise_()
        self.senha.raise_()
        self.usuario.raise_()
        self.label_3.raise_()
        self.bt_vsenha.raise_()
        self.bt_login.raise_()
        self.horizontalLayout.addWidget(self.frame_2, 0, QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.usuario, self.senha)
        MainWindow.setTabOrder(self.senha, self.bt_vsenha)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "SENALAR DISTRIBUIDORA"))
        self.label_3.setText(_translate("MainWindow", "Login"))
        self.senha.setPlaceholderText(_translate("MainWindow", "CPF"))
        self.usuario.setPlaceholderText(_translate("MainWindow", "RA"))
        self.bt_login.setText(_translate("MainWindow", "LOGIN"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_login()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
