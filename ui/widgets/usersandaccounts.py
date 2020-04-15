# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'usersandaccounts.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(344, 394)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.labelsLayout = QtWidgets.QHBoxLayout()
        self.labelsLayout.setObjectName("labelsLayout")
        self.usersLabel = QtWidgets.QLabel(self.centralwidget)
        self.usersLabel.setObjectName("usersLabel")
        self.labelsLayout.addWidget(self.usersLabel)
        self.accountsLabel = QtWidgets.QLabel(self.centralwidget)
        self.accountsLabel.setObjectName("accountsLabel")
        self.labelsLayout.addWidget(self.accountsLabel)
        self.verticalLayout.addLayout(self.labelsLayout)
        self.usersAndAccountsLists = QtWidgets.QHBoxLayout()
        self.usersAndAccountsLists.setObjectName("usersAndAccountsLists")
        self.usersList = QtWidgets.QListView(self.centralwidget)
        self.usersList.setObjectName("usersList")
        self.usersAndAccountsLists.addWidget(self.usersList)
        self.accountsList = QtWidgets.QListView(self.centralwidget)
        self.accountsList.setObjectName("accountsList")
        self.usersAndAccountsLists.addWidget(self.accountsList)
        self.verticalLayout.addLayout(self.usersAndAccountsLists)
        self.propsLabel = QtWidgets.QLabel(self.centralwidget)
        self.propsLabel.setObjectName("propsLabel")
        self.verticalLayout.addWidget(self.propsLabel)
        self.propsList = QtWidgets.QListView(self.centralwidget)
        self.propsList.setObjectName("propsList")
        self.verticalLayout.addWidget(self.propsList)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 344, 21))
        self.menubar.setObjectName("menubar")
        self.menuMenu = QtWidgets.QMenu(self.menubar)
        self.menuMenu.setObjectName("menuMenu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.createUserMenubar = QtWidgets.QAction(MainWindow)
        self.createUserMenubar.setObjectName("createUserMenubar")
        self.createAccountMenubar = QtWidgets.QAction(MainWindow)
        self.createAccountMenubar.setObjectName("createAccountMenubar")
        self.menuMenu.addAction(self.createUserMenubar)
        self.menuMenu.addAction(self.createAccountMenubar)
        self.menubar.addAction(self.menuMenu.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Users & Accounts"))
        self.usersLabel.setText(_translate("MainWindow", "Users"))
        self.accountsLabel.setText(_translate("MainWindow", "Accounts"))
        self.propsLabel.setText(_translate("MainWindow", "Props"))
        self.menuMenu.setTitle(_translate("MainWindow", "Menu"))
        self.createUserMenubar.setText(_translate("MainWindow", "Create User"))
        self.createAccountMenubar.setText(_translate("MainWindow", "Create Account"))
