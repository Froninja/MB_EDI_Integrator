# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Python34\Lib\site-packages\pyqt5\AddCustomer.ui'
#
# Created: Thu Nov 10 20:08:24 2016
#      by: PyQt5 UI code generator 5.3.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_AddCustomerDialog(object):
    def setupUi(self, AddCustomerDialog):
        AddCustomerDialog.setObjectName("AddCustomerDialog")
        AddCustomerDialog.resize(400, 348)
        self.formLayout = QtWidgets.QFormLayout(AddCustomerDialog)
        self.formLayout.setObjectName("formLayout")
        self.NameEdit = QtWidgets.QLineEdit(AddCustomerDialog)
        self.NameEdit.setObjectName("NameEdit")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.NameEdit)
        self.Asset_DepartmentEdit = QtWidgets.QLineEdit(AddCustomerDialog)
        self.Asset_DepartmentEdit.setObjectName("Asset_DepartmentEdit")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.Asset_DepartmentEdit)
        self.Memo_DepartmentEdit = QtWidgets.QLineEdit(AddCustomerDialog)
        self.Memo_DepartmentEdit.setObjectName("Memo_DepartmentEdit")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.Memo_DepartmentEdit)
        self.PO_IDEdit = QtWidgets.QLineEdit(AddCustomerDialog)
        self.PO_IDEdit.setObjectName("PO_IDEdit")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.PO_IDEdit)
        self.label = QtWidgets.QLabel(AddCustomerDialog)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.label_2 = QtWidgets.QLabel(AddCustomerDialog)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.label_3 = QtWidgets.QLabel(AddCustomerDialog)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.label_4 = QtWidgets.QLabel(AddCustomerDialog)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.label_5 = QtWidgets.QLabel(AddCustomerDialog)
        self.label_5.setObjectName("label_5")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_5)
        self.label_6 = QtWidgets.QLabel(AddCustomerDialog)
        self.label_6.setObjectName("label_6")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.label_6)
        self.label_7 = QtWidgets.QLabel(AddCustomerDialog)
        self.label_7.setObjectName("label_7")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.label_7)
        self.label_8 = QtWidgets.QLabel(AddCustomerDialog)
        self.label_8.setObjectName("label_8")
        self.formLayout.setWidget(7, QtWidgets.QFormLayout.LabelRole, self.label_8)
        self.label_9 = QtWidgets.QLabel(AddCustomerDialog)
        self.label_9.setObjectName("label_9")
        self.formLayout.setWidget(8, QtWidgets.QFormLayout.LabelRole, self.label_9)
        self.label_10 = QtWidgets.QLabel(AddCustomerDialog)
        self.label_10.setObjectName("label_10")
        self.formLayout.setWidget(9, QtWidgets.QFormLayout.LabelRole, self.label_10)
        self.label_11 = QtWidgets.QLabel(AddCustomerDialog)
        self.label_11.setObjectName("label_11")
        self.formLayout.setWidget(10, QtWidgets.QFormLayout.LabelRole, self.label_11)
        self.ASN_IDEdit = QtWidgets.QLineEdit(AddCustomerDialog)
        self.ASN_IDEdit.setObjectName("ASN_IDEdit")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.ASN_IDEdit)
        self.Invoice_IDEdit = QtWidgets.QLineEdit(AddCustomerDialog)
        self.Invoice_IDEdit.setObjectName("Invoice_IDEdit")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.Invoice_IDEdit)
        self.ASN_FileEdit = QtWidgets.QLineEdit(AddCustomerDialog)
        self.ASN_FileEdit.setObjectName("ASN_FileEdit")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.ASN_FileEdit)
        self.Invoice_FileEdit = QtWidgets.QLineEdit(AddCustomerDialog)
        self.Invoice_FileEdit.setObjectName("Invoice_FileEdit")
        self.formLayout.setWidget(7, QtWidgets.QFormLayout.FieldRole, self.Invoice_FileEdit)
        self.EDI_VersionEdit = QtWidgets.QLineEdit(AddCustomerDialog)
        self.EDI_VersionEdit.setObjectName("EDI_VersionEdit")
        self.formLayout.setWidget(8, QtWidgets.QFormLayout.FieldRole, self.EDI_VersionEdit)
        self.Creation_Date_RequiredEdit = QtWidgets.QComboBox(AddCustomerDialog)
        self.Creation_Date_RequiredEdit.setObjectName("Creation_Date_RequiredEdit")
        self.formLayout.setWidget(9, QtWidgets.QFormLayout.FieldRole, self.Creation_Date_RequiredEdit)
        self.Description_RequiredEdit = QtWidgets.QComboBox(AddCustomerDialog)
        self.Description_RequiredEdit.setObjectName("Description_RequiredEdit")
        self.formLayout.setWidget(10, QtWidgets.QFormLayout.FieldRole, self.Description_RequiredEdit)
        self.ConfirmButton = QtWidgets.QPushButton(AddCustomerDialog)
        self.ConfirmButton.setObjectName("ConfirmButton")
        self.formLayout.setWidget(11, QtWidgets.QFormLayout.FieldRole, self.ConfirmButton)
        self.CancelButton = QtWidgets.QPushButton(AddCustomerDialog)
        self.CancelButton.setObjectName("CancelButton")
        self.formLayout.setWidget(12, QtWidgets.QFormLayout.FieldRole, self.CancelButton)

        self.retranslateUi(AddCustomerDialog)
        QtCore.QMetaObject.connectSlotsByName(AddCustomerDialog)

    def retranslateUi(self, AddCustomerDialog):
        _translate = QtCore.QCoreApplication.translate
        AddCustomerDialog.setWindowTitle(_translate("AddCustomerDialog", "Dialog"))
        self.label.setText(_translate("AddCustomerDialog", "Name"))
        self.label_2.setText(_translate("AddCustomerDialog", "Asset Department"))
        self.label_3.setText(_translate("AddCustomerDialog", "Memo Department"))
        self.label_4.setText(_translate("AddCustomerDialog", "PO ID"))
        self.label_5.setText(_translate("AddCustomerDialog", "ASN ID"))
        self.label_6.setText(_translate("AddCustomerDialog", "Invoice ID"))
        self.label_7.setText(_translate("AddCustomerDialog", "ASN File"))
        self.label_8.setText(_translate("AddCustomerDialog", "Invoice File"))
        self.label_9.setText(_translate("AddCustomerDialog", "EDI Version"))
        self.label_10.setText(_translate("AddCustomerDialog", "Creation Date Required"))
        self.label_11.setText(_translate("AddCustomerDialog", "Description Required"))
        self.ConfirmButton.setText(_translate("AddCustomerDialog", "Confirm"))
        self.CancelButton.setText(_translate("AddCustomerDialog", "Cancel"))

