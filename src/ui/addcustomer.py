from src.ui.pyuic.UiAddCustomerDialog import Ui_AddCustomerDialog
from PyQt5 import QtGui

class AddCustomerDialog(Ui_AddCustomerDialog):
    def __init__(self, main_window):
        super(AddCustomerDialog, self).__init__()
        self.parent = main_window
        self.setupUi(main_window)
        main_window.setWindowTitle("Add Customer")
        main_window.setWindowIcon(QtGui.QIcon("Resources\\MBIcon.bmp"))
        self.Creation_Date_RequiredEdit = add_options(self.Creation_Date_RequiredEdit)
        self.Description_RequiredEdit = add_options(self.Description_RequiredEdit)
        self.ConfirmButton.clicked.connect(self.confirm_clicked)
        self.CancelButton.clicked.connect(self.cancel_clicked)
        self.customer = dict()
        self.confirmed = False

    def confirm_clicked(self):
        self.customer['Name'] = self.NameEdit.text()
        self.customer['Asset Department'] = self.Asset_DepartmentEdit.text()
        self.customer['Memo Department'] = self.Memo_DepartmentEdit.text()
        self.customer['PO ID'] = self.PO_IDEdit.text()
        self.customer['ASN ID'] = self.ASN_IDEdit.text()
        self.customer['Invoice ID'] = self.Invoice_IDEdit.text()
        self.customer['ASN File'] = self.ASN_FileEdit.text()
        self.customer['Invoice File'] = self.Invoice_FileEdit.text()
        self.customer['EDI Version'] = self.EDI_VersionEdit.text()
        self.customer['Creation Date Required'] = self.Creation_Date_RequiredEdit.currentText()
        self.customer['Description Required'] = self.Description_RequiredEdit.currentText()
        self.confirmed = True
        self.parent.close()

    def cancel_clicked(self):
        self.parent.close()

def add_options(widget):
    widget.addItem("True")
    widget.addItem("False")
    widget.setCurrentIndex(1)
    return widget