# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UPCWarning.ui'
#
# Created: Sun Jun 12 09:09:14 2016
#      by: PyQt5 UI code generator 5.3.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 300)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.WarningLabel = QtWidgets.QLabel(Dialog)
        self.WarningLabel.setObjectName("WarningLabel")
        self.verticalLayout.addWidget(self.WarningLabel)
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setObjectName("label_4")
        self.verticalLayout.addWidget(self.label_4)
        self.tableWidget = QtWidgets.QTableWidget(Dialog)
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setRowCount(0)
        self.verticalLayout.addWidget(self.tableWidget)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.IgnoreButton = QtWidgets.QPushButton(Dialog)
        self.IgnoreButton.setObjectName("IgnoreButton")
        self.gridLayout.addWidget(self.IgnoreButton, 0, 0, 1, 1)
        self.CancelButton = QtWidgets.QPushButton(Dialog)
        self.CancelButton.setObjectName("CancelButton")
        self.gridLayout.addWidget(self.CancelButton, 0, 2, 1, 1)
        self.ConfirmButton = QtWidgets.QPushButton(Dialog)
        self.ConfirmButton.setObjectName("ConfirmButton")
        self.gridLayout.addWidget(self.ConfirmButton, 0, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "UPC Warning"))
        self.WarningLabel.setText(_translate("Dialog", "UPCWarning"))
        self.label_2.setText(_translate("Dialog",
                                        "Press Ignore to ignore this warning and continue with the\
                                        original UPC"))
        self.label_3.setText(_translate("Dialog",
                                        "Select a UPC below and press Confirm to continue with the\
                                        selected UPC"))
        self.label_4.setText(_translate("Dialog", "Press Cancel to cancel the operation"))
        self.IgnoreButton.setText(_translate("Dialog", "Ignore"))
        self.CancelButton.setText(_translate("Dialog", "Cancel"))
        self.ConfirmButton.setText(_translate("Dialog", "Confirm"))
