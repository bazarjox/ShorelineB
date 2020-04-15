# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'createAccount.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(240, 320)
        Dialog.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.usernameLabel = QtWidgets.QLabel(Dialog)
        self.usernameLabel.setGeometry(QtCore.QRect(10, 10, 221, 16))
        self.usernameLabel.setObjectName("usernameLabel")
        self.username = QtWidgets.QLineEdit(Dialog)
        self.username.setGeometry(QtCore.QRect(10, 30, 221, 20))
        self.username.setInputMask("")
        self.username.setText("")
        self.username.setObjectName("username")
        self.passwordLabel = QtWidgets.QLabel(Dialog)
        self.passwordLabel.setGeometry(QtCore.QRect(10, 60, 221, 16))
        self.passwordLabel.setObjectName("passwordLabel")
        self.password = QtWidgets.QLineEdit(Dialog)
        self.password.setGeometry(QtCore.QRect(10, 80, 221, 20))
        self.password.setObjectName("password")
        self.steamapiLabel = QtWidgets.QLabel(Dialog)
        self.steamapiLabel.setGeometry(QtCore.QRect(10, 110, 221, 16))
        self.steamapiLabel.setObjectName("steamapiLabel")
        self.steamapikey = QtWidgets.QLineEdit(Dialog)
        self.steamapikey.setGeometry(QtCore.QRect(10, 130, 221, 20))
        self.steamapikey.setObjectName("steamapikey")
        self.tmapiLabel = QtWidgets.QLabel(Dialog)
        self.tmapiLabel.setGeometry(QtCore.QRect(10, 160, 221, 16))
        self.tmapiLabel.setObjectName("tmapiLabel")
        self.tmapikey = QtWidgets.QLineEdit(Dialog)
        self.tmapikey.setGeometry(QtCore.QRect(10, 180, 221, 20))
        self.tmapikey.setObjectName("tmapikey")
        self.steamidLabel = QtWidgets.QLabel(Dialog)
        self.steamidLabel.setGeometry(QtCore.QRect(10, 210, 221, 16))
        self.steamidLabel.setObjectName("steamidLabel")
        self.steamid = QtWidgets.QLineEdit(Dialog)
        self.steamid.setGeometry(QtCore.QRect(10, 230, 221, 20))
        self.steamid.setObjectName("steamid")
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(80, 260, 75, 23))
        self.pushButton.setObjectName("pushButton")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Create Account"))
        self.usernameLabel.setText(_translate("Dialog", "Username"))
        self.username.setPlaceholderText(_translate("Dialog", "Enter Steam username..."))
        self.passwordLabel.setText(_translate("Dialog", "Password"))
        self.password.setPlaceholderText(_translate("Dialog", "Enter Steam password..."))
        self.steamapiLabel.setText(_translate("Dialog", "Steam API Key (click to get it)"))
        self.steamapikey.setPlaceholderText(_translate("Dialog", "Enter Steam API key"))
        self.tmapiLabel.setText(_translate("Dialog", "TM market.csgo.com API Key"))
        self.tmapikey.setPlaceholderText(_translate("Dialog", "Enter TM API Key"))
        self.steamidLabel.setText(_translate("Dialog", "Your profile url or SteamID"))
        self.steamid.setPlaceholderText(_translate("Dialog", "ex: https://steamcommunity.com/profiles/76561198983927239"))
        self.pushButton.setText(_translate("Dialog", "Check"))
