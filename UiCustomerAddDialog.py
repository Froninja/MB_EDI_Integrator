from PyQt5 import QtCore, QtGui, QtWidgets
from CustomerSettings import CustomerSettings
import sys

class Ui_CustomerAddDialog(object):
    def setupUi(self, CustomerAddDialog):
        CustomerAddDialog.setObjectName("CustomerAddDialog")
        self.parent = CustomerAddDialog
        self.parent.setWindowIcon(QtGui.QIcon("Resources\MBIcon.bmp"))
        self.confirmed = False
        self.gridLayout = QtWidgets.QGridLayout(CustomerAddDialog)
        self.gridLayout.setObjectName("gridLayout")
        index = 0
        for setting in CustomerSettings().sorted_dict():
            self.label = QtWidgets.QLabel(CustomerAddDialog)
            self.label.setObjectName(setting + "_label")
            self.label.setText(setting[2:].replace('_',' ').title())
            self.gridLayout.addWidget(self.label, index, 0, 1, 1)
            self.line = QtWidgets.QLineEdit(CustomerAddDialog)
            self.line.setObjectName(setting + "_line")
            self.gridLayout.addWidget(self.line, index, 1, 1, 1)
            index += 1
        self.confirmButton = QtWidgets.QPushButton(CustomerAddDialog)
        self.confirmButton.setObjectName("ConfirmButton")
        self.confirmButton.setText("Confirm")
        self.confirmButton.clicked.connect(self.confirm_clicked)
        self.gridLayout.addWidget(self.confirmButton, index, 0, 1, 1)
        self.cancelButton = QtWidgets.QPushButton(CustomerAddDialog)
        self.cancelButton.setObjectName("CancelName")
        self.cancelButton.setText("Cancel")
        self.cancelButton.clicked.connect(self.cancel_clicked)
        self.gridLayout.addWidget(self.cancelButton, index, 1, 1, 1)
        CustomerAddDialog.setWindowTitle("Add New Customer")

    def confirm_clicked(self):
        self.customer = CustomerSettings()
        for setting in self.customer.sorted_dict():
            setattr(self.customer, setting, self.parent.findChild(QtWidgets.QLineEdit, setting + "_line").text())
        self.confirmed = True
        self.parent.close()

    def cancel_clicked(self):
        self.parent.close()

if __name__ == '__main__':
    a = QtWidgets.QApplication(sys.argv)
    q = QtWidgets.QDialog()
    w = Ui_CustomerAddDialog()
    w.setupUi(q)
    q.show()

    sys.exit(a.exec_())