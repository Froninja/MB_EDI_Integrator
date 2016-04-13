# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mb_edi_settings_2.ui'
#
# Created by: PyQt5 UI code generator 5.5
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_SettingsDialog(object):
    def setupUi(self, SettingsDialog):
        SettingsDialog.setObjectName("SettingsDialog")
        SettingsDialog.resize(400, 705)
        self.verticalLayout = QtWidgets.QVBoxLayout(SettingsDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame = QtWidgets.QFrame(SettingsDialog)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame.setObjectName("frame")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.frame)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.CustomerTable = QtWidgets.QTableView(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.CustomerTable.sizePolicy().hasHeightForWidth())
        self.CustomerTable.setSizePolicy(sizePolicy)
        self.CustomerTable.setObjectName("CustomerTable")
        self.gridLayout_2.addWidget(self.CustomerTable, 1, 0, 1, 1)
        self.frame_5 = QtWidgets.QFrame(self.frame)
        self.frame_5.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_5.setObjectName("frame_5")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame_5)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.AddCustomerButton = QtWidgets.QPushButton(self.frame_5)
        self.AddCustomerButton.setObjectName("AddCustomerButton")
        self.horizontalLayout_2.addWidget(self.AddCustomerButton)
        self.DeleteCustomerButton = QtWidgets.QPushButton(self.frame_5)
        self.DeleteCustomerButton.setObjectName("DeleteCustomerButton")
        self.horizontalLayout_2.addWidget(self.DeleteCustomerButton)
        self.gridLayout_2.addWidget(self.frame_5, 0, 0, 1, 1)
        self.verticalLayout.addWidget(self.frame)
        self.frame_2 = QtWidgets.QFrame(SettingsDialog)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame_2.setObjectName("frame_2")
        self.gridLayout = QtWidgets.QGridLayout(self.frame_2)
        self.gridLayout.setObjectName("gridLayout")
        self.DescLogButton = QtWidgets.QToolButton(self.frame_2)
        self.DescLogButton.setObjectName("DescLogButton")
        self.gridLayout.addWidget(self.DescLogButton, 2, 2, 1, 1)
        self.DestLogLabel = QtWidgets.QLabel(self.frame_2)
        self.DestLogLabel.setObjectName("DestLogLabel")
        self.gridLayout.addWidget(self.DestLogLabel, 1, 0, 1, 1)
        self.LabelRecordButton = QtWidgets.QToolButton(self.frame_2)
        self.LabelRecordButton.setObjectName("LabelRecordButton")
        self.gridLayout.addWidget(self.LabelRecordButton, 4, 2, 1, 1)
        self.DestLogLine = QtWidgets.QLineEdit(self.frame_2)
        self.DestLogLine.setObjectName("DestLogLine")
        self.gridLayout.addWidget(self.DestLogLine, 1, 1, 1, 1)
        self.LabelRecordLine = QtWidgets.QLineEdit(self.frame_2)
        self.LabelRecordLine.setObjectName("LabelRecordLine")
        self.gridLayout.addWidget(self.LabelRecordLine, 4, 1, 1, 1)
        self.UPCExceptButton = QtWidgets.QToolButton(self.frame_2)
        self.UPCExceptButton.setObjectName("UPCExceptButton")
        self.gridLayout.addWidget(self.UPCExceptButton, 3, 2, 1, 1)
        self.ShipLogLabel = QtWidgets.QLabel(self.frame_2)
        self.ShipLogLabel.setObjectName("ShipLogLabel")
        self.gridLayout.addWidget(self.ShipLogLabel, 0, 0, 1, 1)
        self.DestLogButton = QtWidgets.QToolButton(self.frame_2)
        self.DestLogButton.setObjectName("DestLogButton")
        self.gridLayout.addWidget(self.DestLogButton, 1, 2, 1, 1)
        self.ShipLogLine = QtWidgets.QLineEdit(self.frame_2)
        self.ShipLogLine.setObjectName("ShipLogLine")
        self.gridLayout.addWidget(self.ShipLogLine, 0, 1, 1, 1)
        self.DescLogLabel = QtWidgets.QLabel(self.frame_2)
        self.DescLogLabel.setObjectName("DescLogLabel")
        self.gridLayout.addWidget(self.DescLogLabel, 2, 0, 1, 1)
        self.ShipLogButton = QtWidgets.QToolButton(self.frame_2)
        self.ShipLogButton.setObjectName("ShipLogButton")
        self.gridLayout.addWidget(self.ShipLogButton, 0, 2, 1, 1)
        self.DescLogLine = QtWidgets.QLineEdit(self.frame_2)
        self.DescLogLine.setObjectName("DescLogLine")
        self.gridLayout.addWidget(self.DescLogLine, 2, 1, 1, 1)
        self.UPCExceptLabel = QtWidgets.QLabel(self.frame_2)
        self.UPCExceptLabel.setObjectName("UPCExceptLabel")
        self.gridLayout.addWidget(self.UPCExceptLabel, 3, 0, 1, 1)
        self.LabelRecordLabel = QtWidgets.QLabel(self.frame_2)
        self.LabelRecordLabel.setObjectName("LabelRecordLabel")
        self.gridLayout.addWidget(self.LabelRecordLabel, 4, 0, 1, 1)
        self.UPCExceptLine = QtWidgets.QLineEdit(self.frame_2)
        self.UPCExceptLine.setObjectName("UPCExceptLine")
        self.gridLayout.addWidget(self.UPCExceptLine, 3, 1, 1, 1)
        self.MapdataLabel = QtWidgets.QLabel(self.frame_2)
        self.MapdataLabel.setObjectName("MapdataLabel")
        self.gridLayout.addWidget(self.MapdataLabel, 5, 0, 1, 1)
        self.MapdataLine = QtWidgets.QLineEdit(self.frame_2)
        self.MapdataLine.setObjectName("MapdataLine")
        self.gridLayout.addWidget(self.MapdataLine, 5, 1, 1, 1)
        self.MapdataButton = QtWidgets.QToolButton(self.frame_2)
        self.MapdataButton.setObjectName("MapdataButton")
        self.gridLayout.addWidget(self.MapdataButton, 5, 2, 1, 1)
        self.POdataLine = QtWidgets.QLineEdit(self.frame_2)
        self.POdataLine.setObjectName("POdataLine")
        self.gridLayout.addWidget(self.POdataLine, 6, 1, 1, 1)
        self.POdataLabel = QtWidgets.QLabel(self.frame_2)
        self.POdataLabel.setObjectName("POdataLabel")
        self.gridLayout.addWidget(self.POdataLabel, 6, 0, 1, 1)
        self.POdataButton = QtWidgets.QToolButton(self.frame_2)
        self.POdataButton.setObjectName("POdataButton")
        self.gridLayout.addWidget(self.POdataButton, 6, 2, 1, 1)
        self.verticalLayout.addWidget(self.frame_2)
        self.frame_3 = QtWidgets.QFrame(SettingsDialog)
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame_3.setObjectName("frame_3")
        self.formLayout = QtWidgets.QFormLayout(self.frame_3)
        self.formLayout.setObjectName("formLayout")
        self.UPCQueryLine = QtWidgets.QLineEdit(self.frame_3)
        self.UPCQueryLine.setObjectName("UPCQueryLine")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.UPCQueryLine)
        self.RingUPCQueryLine = QtWidgets.QLineEdit(self.frame_3)
        self.RingUPCQueryLine.setObjectName("RingUPCQueryLine")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.RingUPCQueryLine)
        self.UPCQueryLabel = QtWidgets.QLabel(self.frame_3)
        self.UPCQueryLabel.setObjectName("UPCQueryLabel")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.UPCQueryLabel)
        self.RingUPCQueryLabel = QtWidgets.QLabel(self.frame_3)
        self.RingUPCQueryLabel.setObjectName("RingUPCQueryLabel")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.RingUPCQueryLabel)
        self.MemDestQueryLine = QtWidgets.QLineEdit(self.frame_3)
        self.MemDestQueryLine.setObjectName("MemDestQueryLine")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.MemDestQueryLine)
        self.DestQueryLine = QtWidgets.QLineEdit(self.frame_3)
        self.DestQueryLine.setObjectName("DestQueryLine")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.DestQueryLine)
        self.InvQueryLine = QtWidgets.QLineEdit(self.frame_3)
        self.InvQueryLine.setObjectName("InvQueryLine")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.InvQueryLine)
        self.ConnLine = QtWidgets.QLineEdit(self.frame_3)
        self.ConnLine.setObjectName("ConnLine")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.ConnLine)
        self.MemDestQueryLabel = QtWidgets.QLabel(self.frame_3)
        self.MemDestQueryLabel.setObjectName("MemDestQueryLabel")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.MemDestQueryLabel)
        self.DestQueryLabel = QtWidgets.QLabel(self.frame_3)
        self.DestQueryLabel.setObjectName("DestQueryLabel")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.DestQueryLabel)
        self.InvQueryLabel = QtWidgets.QLabel(self.frame_3)
        self.InvQueryLabel.setObjectName("InvQueryLabel")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.InvQueryLabel)
        self.ConnLabel = QtWidgets.QLabel(self.frame_3)
        self.ConnLabel.setObjectName("ConnLabel")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.ConnLabel)
        self.verticalLayout.addWidget(self.frame_3)
        self.frame_6 = QtWidgets.QFrame(SettingsDialog)
        self.frame_6.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame_6.setObjectName("frame_6")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame_6)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.StatusLabel = QtWidgets.QLabel(self.frame_6)
        self.StatusLabel.setObjectName("StatusLabel")
        self.verticalLayout_2.addWidget(self.StatusLabel)
        self.StatusList = QtWidgets.QTableWidget(self.frame_6)
        self.StatusList.setColumnCount(1)
        self.StatusList.setObjectName("StatusList")
        self.StatusList.setRowCount(0)
        self.StatusList.horizontalHeader().setVisible(False)
        self.StatusList.horizontalHeader().setStretchLastSection(True)
        self.verticalLayout_2.addWidget(self.StatusList)
        self.verticalLayout.addWidget(self.frame_6)
        self.frame_4 = QtWidgets.QFrame(SettingsDialog)
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame_4.setObjectName("frame_4")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame_4)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.AcceptButton = QtWidgets.QPushButton(self.frame_4)
        self.AcceptButton.setObjectName("AcceptButton")
        self.horizontalLayout.addWidget(self.AcceptButton)
        self.CancelButton = QtWidgets.QPushButton(self.frame_4)
        self.CancelButton.setObjectName("CancelButton")
        self.horizontalLayout.addWidget(self.CancelButton)
        self.verticalLayout.addWidget(self.frame_4)

        self.retranslateUi(SettingsDialog)
        QtCore.QMetaObject.connectSlotsByName(SettingsDialog)

    def retranslateUi(self, SettingsDialog):
        _translate = QtCore.QCoreApplication.translate
        SettingsDialog.setWindowTitle(_translate("SettingsDialog", "Settings"))
        self.AddCustomerButton.setText(_translate("SettingsDialog", "Add New Customer"))
        self.DeleteCustomerButton.setText(_translate("SettingsDialog", "Delete Customer"))
        self.DescLogButton.setText(_translate("SettingsDialog", "..."))
        self.DestLogLabel.setText(_translate("SettingsDialog", "Destination Log"))
        self.LabelRecordButton.setText(_translate("SettingsDialog", "..."))
        self.UPCExceptButton.setText(_translate("SettingsDialog", "..."))
        self.ShipLogLabel.setText(_translate("SettingsDialog", "Shipping Log"))
        self.DestLogButton.setText(_translate("SettingsDialog", "..."))
        self.DescLogLabel.setText(_translate("SettingsDialog", "Description Log"))
        self.ShipLogButton.setText(_translate("SettingsDialog", "..."))
        self.UPCExceptLabel.setText(_translate("SettingsDialog", "UPC Exception File"))
        self.LabelRecordLabel.setText(_translate("SettingsDialog", "Label Record File"))
        self.MapdataLabel.setText(_translate("SettingsDialog", "MAPDATA Path"))
        self.MapdataButton.setText(_translate("SettingsDialog", "..."))
        self.POdataLabel.setText(_translate("SettingsDialog", "PO Database"))
        self.POdataButton.setText(_translate("SettingsDialog", "..."))
        self.UPCQueryLabel.setText(_translate("SettingsDialog", "Non-Ring UPC Query"))
        self.RingUPCQueryLabel.setText(_translate("SettingsDialog", "Ring UPC Query"))
        self.MemDestQueryLabel.setText(_translate("SettingsDialog", "Memo Destination Query"))
        self.DestQueryLabel.setText(_translate("SettingsDialog", "Destination Query"))
        self.InvQueryLabel.setText(_translate("SettingsDialog", "Invoice Query"))
        self.ConnLabel.setText(_translate("SettingsDialog", "Connection String"))
        self.StatusLabel.setText(_translate("SettingsDialog", "Status Options"))
        self.AcceptButton.setText(_translate("SettingsDialog", "Accept"))
        self.CancelButton.setText(_translate("SettingsDialog", "Cancel"))

