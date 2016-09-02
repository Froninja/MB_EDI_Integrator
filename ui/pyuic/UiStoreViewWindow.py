# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MB_EDI_StoreView.ui'
#
# Created by: PyQt5 UI code generator 5.5
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_StoreViewWindow(object):
    def setupUi(self, StoreViewWindow):
        StoreViewWindow.setObjectName("StoreViewWindow")
        StoreViewWindow.resize(600, 500)
        self.centralwidget = QtWidgets.QWidget(StoreViewWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.StoreView = QtWidgets.QTreeView(self.centralwidget)
        self.StoreView.setObjectName("StoreView")
        self.horizontalLayout.addWidget(self.StoreView)
        StoreViewWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(StoreViewWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 600, 21))
        self.menubar.setObjectName("menubar")
        self.menuExport = QtWidgets.QMenu(self.menubar)
        self.menuExport.setObjectName("menuExport")
        StoreViewWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(StoreViewWindow)
        self.statusbar.setObjectName("statusbar")
        StoreViewWindow.setStatusBar(self.statusbar)
        self.actionExport_Spreadsheet = QtWidgets.QAction(StoreViewWindow)
        self.actionExport_Spreadsheet.setObjectName("actionExport_Spreadsheet")
        self.actionExport_for_Print = QtWidgets.QAction(StoreViewWindow)
        self.actionExport_for_Print.setObjectName("actionExport_for_Print")
        self.menuExport.addAction(self.actionExport_Spreadsheet)
        self.menuExport.addAction(self.actionExport_for_Print)
        self.menubar.addAction(self.menuExport.menuAction())

        self.retranslateUi(StoreViewWindow)
        QtCore.QMetaObject.connectSlotsByName(StoreViewWindow)

    def retranslateUi(self, StoreViewWindow):
        _translate = QtCore.QCoreApplication.translate
        StoreViewWindow.setWindowTitle(_translate("StoreViewWindow", "MainWindow"))
        self.menuExport.setTitle(_translate("StoreViewWindow", "Export"))
        self.actionExport_Spreadsheet.setText(_translate("StoreViewWindow", "Export Spreadsheet"))
        self.actionExport_for_Print.setText(_translate("StoreViewWindow", "Export for Print"))

