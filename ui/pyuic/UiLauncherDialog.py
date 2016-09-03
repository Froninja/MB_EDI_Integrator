# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MB_EDI_Launcher.ui'
#
# Created by: PyQt5 UI code generator 5.5
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Launcher(object):
    def setupUi(self, Launcher):
        Launcher.setObjectName("Launcher")
        Launcher.resize(618, 376)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Launcher.sizePolicy().hasHeightForWidth())
        Launcher.setSizePolicy(sizePolicy)
        Launcher.setAutoFillBackground(False)
        self.verticalLayout = QtWidgets.QVBoxLayout(Launcher)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_2 = QtWidgets.QLabel(Launcher)
        self.label_2.setMaximumSize(QtCore.QSize(600, 40))
        self.label_2.setAutoFillBackground(False)
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap("Resources/MBLogo.png"))
        self.label_2.setScaledContents(True)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.label = QtWidgets.QLabel(Launcher)
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        self.label.setFont(font)
        self.label.setTextFormat(QtCore.Qt.AutoText)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.frame = QtWidgets.QFrame(Launcher)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.ShipButton = QtWidgets.QPushButton(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ShipButton.sizePolicy().hasHeightForWidth())
        self.ShipButton.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(12)
        self.ShipButton.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("Resources/5-512.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ShipButton.setIcon(icon)
        self.ShipButton.setIconSize(QtCore.QSize(60, 60))
        self.ShipButton.setObjectName("ShipButton")
        self.horizontalLayout.addWidget(self.ShipButton)
        self.POButton = QtWidgets.QPushButton(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.POButton.sizePolicy().hasHeightForWidth())
        self.POButton.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(12)
        self.POButton.setFont(font)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("Resources/Notepad-512.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.POButton.setIcon(icon1)
        self.POButton.setIconSize(QtCore.QSize(60, 60))
        self.POButton.setObjectName("POButton")
        self.horizontalLayout.addWidget(self.POButton)
        self.ShipLogButton = QtWidgets.QPushButton(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ShipLogButton.sizePolicy().hasHeightForWidth())
        self.ShipLogButton.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(12)
        self.ShipLogButton.setFont(font)
        self.ShipLogButton.setLayoutDirection(QtCore.Qt.LeftToRight)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("Resources/todo_list-512.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ShipLogButton.setIcon(icon2)
        self.ShipLogButton.setIconSize(QtCore.QSize(60, 60))
        self.ShipLogButton.setObjectName("ShipLogButton")
        self.horizontalLayout.addWidget(self.ShipLogButton)
        self.verticalLayout.addWidget(self.frame)
        self.VersionLabel = QtWidgets.QLabel(Launcher)
        self.VersionLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.VersionLabel.setObjectName("VersionLabel")
        self.verticalLayout.addWidget(self.VersionLabel)
        self.verticalLayout.setStretch(0, 1)
        self.verticalLayout.setStretch(1, 1)
        self.verticalLayout.setStretch(2, 3)

        self.retranslateUi(Launcher)
        QtCore.QMetaObject.connectSlotsByName(Launcher)

    def retranslateUi(self, Launcher):
        _translate = QtCore.QCoreApplication.translate
        Launcher.setWindowTitle(_translate("Launcher", "Dialog"))
        self.label.setText(_translate("Launcher", "EDI Integrator 2016"))
        self.ShipButton.setText(_translate("Launcher", "Shipping"))
        self.POButton.setText(_translate("Launcher", "Purchase Orders"))
        self.ShipLogButton.setText(_translate("Launcher", "Shipment Log"))
        self.VersionLabel.setText(_translate("Launcher", "TextLabel"))
