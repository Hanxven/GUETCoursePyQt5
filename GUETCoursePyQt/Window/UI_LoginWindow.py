# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'LoginWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_LoginWindow(object):
    def setupUi(self, LoginWindow):
        LoginWindow.setObjectName("LoginWindow")
        LoginWindow.resize(297, 121)
        LoginWindow.setWindowTitle("")
        LoginWindow.setSizeGripEnabled(False)
        LoginWindow.setModal(True)
        self.gridLayout = QtWidgets.QGridLayout(LoginWindow)
        self.gridLayout.setContentsMargins(3, 3, 3, 3)
        self.gridLayout.setSpacing(3)
        self.gridLayout.setObjectName("gridLayout")
        self.lableC = QtWidgets.QLabel(LoginWindow)
        self.lableC.setObjectName("lableC")
        self.gridLayout.addWidget(self.lableC, 2, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.btnLogin = QtWidgets.QPushButton(LoginWindow)
        self.btnLogin.setObjectName("btnLogin")
        self.horizontalLayout.addWidget(self.btnLogin)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.gridLayout.addLayout(self.horizontalLayout, 4, 0, 1, 2)
        self.labelB = QtWidgets.QLabel(LoginWindow)
        self.labelB.setObjectName("labelB")
        self.gridLayout.addWidget(self.labelB, 1, 0, 1, 1)
        self.labelA = QtWidgets.QLabel(LoginWindow)
        self.labelA.setObjectName("labelA")
        self.gridLayout.addWidget(self.labelA, 0, 0, 1, 1)
        self.lineEditAccount = QtWidgets.QLineEdit(LoginWindow)
        self.lineEditAccount.setObjectName("lineEditAccount")
        self.gridLayout.addWidget(self.lineEditAccount, 0, 1, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.lineEditValidationCode = QtWidgets.QLineEdit(LoginWindow)
        self.lineEditValidationCode.setObjectName("lineEditValidationCode")
        self.horizontalLayout_2.addWidget(self.lineEditValidationCode)
        self.labelCkCode = QtWidgets.QLabel(LoginWindow)
        self.labelCkCode.setAlignment(QtCore.Qt.AlignCenter)
        self.labelCkCode.setObjectName("labelCkCode")
        self.horizontalLayout_2.addWidget(self.labelCkCode)
        self.btnRefresh = QtWidgets.QToolButton(LoginWindow)
        self.btnRefresh.setObjectName("btnRefresh")
        self.horizontalLayout_2.addWidget(self.btnRefresh)
        self.gridLayout.addLayout(self.horizontalLayout_2, 2, 1, 1, 1)
        self.lineEditPasswd = QtWidgets.QLineEdit(LoginWindow)
        self.lineEditPasswd.setObjectName("lineEditPasswd")
        self.gridLayout.addWidget(self.lineEditPasswd, 1, 1, 1, 1)

        self.retranslateUi(LoginWindow)
        QtCore.QMetaObject.connectSlotsByName(LoginWindow)
        LoginWindow.setTabOrder(self.lineEditAccount, self.lineEditPasswd)
        LoginWindow.setTabOrder(self.lineEditPasswd, self.lineEditValidationCode)
        LoginWindow.setTabOrder(self.lineEditValidationCode, self.btnRefresh)
        LoginWindow.setTabOrder(self.btnRefresh, self.btnLogin)

    def retranslateUi(self, LoginWindow):
        _translate = QtCore.QCoreApplication.translate
        self.lableC.setText(_translate("LoginWindow", "?????????"))
        self.btnLogin.setText(_translate("LoginWindow", "??????"))
        self.labelB.setText(_translate("LoginWindow", "??????"))
        self.labelA.setText(_translate("LoginWindow", "??????"))
        self.labelCkCode.setText(_translate("LoginWindow", "Loading..."))
        self.btnRefresh.setText(_translate("LoginWindow", "??????"))
