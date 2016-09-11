from PyQt5 import QtWidgets, QtGui
from src.ui.pyuic.UiUPCWarningDialog import Ui_Dialog
from src.models.purchaseorder import PurchaseOrder, Store, Item
from src.models.invoice import Invoice, Product
import sys

class WarningDialog(QtWidgets.QMessageBox):
    def __init__(self, message, detail=None):
        QtWidgets.QMessageBox.__init__(self)
        self.setWindowTitle("Warning")
        self.setWindowIcon(QtGui.QIcon("Resources\\MBIcon.bmp"))
        self.setText(message)
        self.setInformativeText("Continue or cancel?")
        self.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
        self.setDefaultButton(QtWidgets.QMessageBox.Cancel)
        if detail is not None:
            self.setDetailedText(detail)

class OverWriteDialog(QtWidgets.QMessageBox):
    def __init__(self):
        QtWidgets.QMessageBox.__init__(self)

        self.setWindowTitle("Overwrite?")
        self.setWindowIcon(QtGui.QIcon("Resources\\MBIcon.bmp"))
        self.setText("A previous output file already exists. Do you want to append this file?")
        self.setInformativeText("Caution: Selecting No can overwrite previous work")
        self.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        self.setDefaultButton(QtWidgets.QMessageBox.Yes)

class POWarningDialog(QtWidgets.QDialog):
    def __init__(self, po_num, inv_num):
        QtWidgets.QDialog.__init__(self)
        self.setWindowTitle("PO Warning")
        self.setWindowIcon(QtGui.QIcon("Resources\\MBIcon.bmp"))
        self.vertical_layout = QtWidgets.QVBoxLayout(self)
        self.label = QtWidgets.QLabel(self)
        self.label.setText("PO# %s does not seem to be a valid PO#. Please confirm or enter a new PO#" % po_num)
        self.vertical_layout.addWidget(self.label)
        self.inv_label = QtWidgets.QLabel(self)
        self.inv_label.setText("Invoice(s): %s" % str(inv_num).rstrip(']').lstrip('['))
        self.vertical_layout.addWidget(self.inv_label)
        self.input_box = QtWidgets.QLineEdit(self)
        self.vertical_layout.addWidget(self.input_box)
        self.button_frame = QtWidgets.QFrame()
        self.h_layout = QtWidgets.QHBoxLayout(self.button_frame)
        self.confirm_button = QtWidgets.QPushButton("Confirm", self)
        self.confirm_button.clicked.connect(self.confirm_clicked)
        self.h_layout.addWidget(self.confirm_button)
        self.cancel_button = QtWidgets.QPushButton("Cancel", self)
        self.cancel_button.clicked.connect(self.cancel_clicked)
        self.h_layout.addWidget(self.cancel_button)
        self.vertical_layout.addWidget(self.button_frame)
        self.po_num = ''
        self.confirmed = False

    def confirm_clicked(self):
        """Sets the po_num attribute to the user entered text, sets the confirmed attribute to
        true, and closes the dialog"""
        #if self.input_box.text() != '' or self.input_box.text() != None:
        self.po_num = self.input_box.text()
        self.confirmed = True
        self.close()
        #else:
            #pass

    def cancel_clicked(self):
        """Closes the dialog"""
        self.close()

class UPCWarningDialog(QtWidgets.QDialog):
    def __init__(self, style_num, inv_num):
        QtWidgets.QDialog.__init__(self)
        self.setWindowTitle("UPC Warning")
        self.setWindowIcon(QtGui.QIcon("Resources\\MBIcon.bmp"))
        self.vertical_layout = QtWidgets.QVBoxLayout(self)
        self.label = QtWidgets.QLabel(self)
        self.label.setText("Cannot find a UPC for %s. Please enter the UPC below" % style_num)
        self.vertical_layout.addWidget(self.label)
        self.inv_label = QtWidgets.QLabel(self)
        self.inv_label.setText("Invoice(s): %s" % str(inv_num).rstrip(']').lstrip('['))
        self.vertical_layout.addWidget(self.inv_label)
        self.input_box = QtWidgets.QLineEdit(self)
        self.vertical_layout.addWidget(self.input_box)
        self.button_frame = QtWidgets.QFrame()
        self.h_layout = QtWidgets.QHBoxLayout(self.button_frame)
        self.confirm_button = QtWidgets.QPushButton("Confirm", self)
        self.confirm_button.clicked.connect(self.confirm_clicked)
        self.h_layout.addWidget(self.confirm_button)
        self.cancel_button = QtWidgets.QPushButton("Cancel", self)
        self.cancel_button.clicked.connect(self.cancel_clicked)
        self.h_layout.addWidget(self.cancel_button)
        self.vertical_layout.addWidget(self.button_frame)
        self.upc = ''
        self.confirmed = False

    def confirm_clicked(self):
        if self.input_box.text() != '' or self.input_box.text() != None:
            self.upc = self.input_box.text()
            self.confirmed = True
            self.close()
        else:
            pass

    def cancel_clicked(self):
        self.close()

class TrackingWarningDialog(QtWidgets.QDialog):
    def __init__(self, inv_num):
        QtWidgets.QDialog.__init__(self)
        self.setWindowTitle("Tracking Warning")
        self.setWindowIcon(QtGui.QIcon("Resources\\MBIcon.bmp"))
        self.vertical_layout = QtWidgets.QVBoxLayout(self)
        self.label = QtWidgets.QLabel(self)
        self.label.setText("Cannot find a tracking number for Invoice# %s. Please enter the tracking number below" % inv_num)
        self.vertical_layout.addWidget(self.label)
        self.input_box = QtWidgets.QLineEdit(self)
        self.vertical_layout.addWidget(self.input_box)
        self.button_frame = QtWidgets.QFrame()
        self.h_layout = QtWidgets.QHBoxLayout(self.button_frame)
        self.confirm_button = QtWidgets.QPushButton("Confirm", self)
        self.confirm_button.clicked.connect(self.confirm_clicked)
        self.h_layout.addWidget(self.confirm_button)
        self.cancel_button = QtWidgets.QPushButton("Cancel", self)
        self.cancel_button.clicked.connect(self.cancel_clicked)
        self.h_layout.addWidget(self.cancel_button)
        self.vertical_layout.addWidget(self.button_frame)
        self.tracking = ''
        self.confirmed = False

    def confirm_clicked(self):
        if self.input_box.text() != '' or self.input_box.text() != None:
            self.tracking = self.input_box.text()
            self.confirmed = True
            self.close()
        else:
            pass

    def cancel_clicked(self):
        self.close()

class StoreWarningDialog(QtWidgets.QDialog):
    def __init__(self, dest, inv_num):
        QtWidgets.QDialog.__init__(self)
        self.setWindowTitle("Store Warning")
        self.setWindowIcon(QtGui.QIcon("Resources\\MBIcon.bmp"))
        self.vertical_layout = QtWidgets.QVBoxLayout(self)
        self.label = QtWidgets.QLabel(self)
        self.label.setText("Cannot find a store number for %s. Please enter the info below" % dest)
        self.vertical_layout.addWidget(self.label)
        self.inv_label = QtWidgets.QLabel(self)
        self.inv_label.setText("Invoice(s): %s" % str(inv_num).rstrip(']').lstrip('['))
        self.vertical_layout.addWidget(self.inv_label)
        self.store_label = QtWidgets.QLabel("Store number")
        self.vertical_layout.addWidget(self.store_label)
        self.store_num_box = QtWidgets.QLineEdit(self)
        self.vertical_layout.addWidget(self.store_num_box)
        self.dc_label = QtWidgets.QLabel("Distribution Center Number")
        self.vertical_layout.addWidget(self.dc_label)
        self.dc_num_box = QtWidgets.QLineEdit(self)
        self.vertical_layout.addWidget(self.dc_num_box)
        self.name_label = QtWidgets.QLabel("Store name")
        self.vertical_layout.addWidget(self.name_label)
        self.store_name_box = QtWidgets.QLineEdit(self)
        self.vertical_layout.addWidget(self.store_name_box)
        self.button_frame = QtWidgets.QFrame()
        self.h_layout = QtWidgets.QHBoxLayout(self.button_frame)
        self.confirm_button = QtWidgets.QPushButton("Confirm", self)
        self.confirm_button.clicked.connect(self.confirm_clicked)
        self.h_layout.addWidget(self.confirm_button)
        self.cancel_button = QtWidgets.QPushButton("Cancel", self)
        self.cancel_button.clicked.connect(self.cancel_clicked)
        self.h_layout.addWidget(self.cancel_button)
        self.vertical_layout.addWidget(self.button_frame)
        self.store_num = ''
        self.dc_num = ''
        self.store_name = ''
        self.confirmed = False

    def confirm_clicked(self):
        if self.store_num_box.text() != '' and self.dc_num_box.text() != '':
            self.store_num = self.store_num_box.text().zfill(4)
            self.dc_num = self.dc_num_box.text().zfill(4)
            self.store_name = self.store_name_box.text()
            self.confirmed = True
            self.close()
        else:
            pass

    def cancel_clicked(self):
        self.close()

class DescriptionWarningDialog(QtWidgets.QDialog):
    def __init__(self, upc, style_num, inv_num):
        QtWidgets.QDialog.__init__(self)
        self.setWindowTitle("Warning")
        self.setWindowIcon(QtGui.QIcon("Resources\\MBIcon.bmp"))
        self.vertical_layout = QtWidgets.QVBoxLayout(self)
        self.label = QtWidgets.QLabel(self)
        self.label.setText("Cannot find a description for style %s (UPC %s). Please enter the info below" % (style_num, upc))
        self.vertical_layout.addWidget(self.label)
        self.inv_label = QtWidgets.QLabel(self)
        self.inv_label.setText("Invoice(s): %s" % str(inv_num).rstrip(']').lstrip('['))
        self.vertical_layout.addWidget(self.inv_label)
        self.desc_label = QtWidgets.QLabel("Description")
        self.vertical_layout.addWidget(self.desc_label)
        self.desc_box = QtWidgets.QLineEdit(self)
        self.vertical_layout.addWidget(self.desc_box)
        self.color_label = QtWidgets.QLabel("Color or NONE")
        self.vertical_layout.addWidget(self.color_label)
        self.color_box = QtWidgets.QLineEdit(self)
        self.vertical_layout.addWidget(self.color_box)
        self.size_label = QtWidgets.QLabel("Size or NONE")
        self.vertical_layout.addWidget(self.size_label)
        self.size_box = QtWidgets.QLineEdit(self)
        self.vertical_layout.addWidget(self.size_box)
        self.button_frame = QtWidgets.QFrame()
        self.h_layout = QtWidgets.QHBoxLayout(self.button_frame)
        self.confirm_button = QtWidgets.QPushButton("Confirm", self)
        self.confirm_button.clicked.connect(self.confirm_clicked)
        self.h_layout.addWidget(self.confirm_button)
        self.cancel_button = QtWidgets.QPushButton("Cancel", self)
        self.cancel_button.clicked.connect(self.cancel_clicked)
        self.h_layout.addWidget(self.cancel_button)
        self.vertical_layout.addWidget(self.button_frame)
        self.description = ''
        self.color = ''
        self.size = ''
        self.confirmed = False

    def confirm_clicked(self):
        if self.desc_box.text() != '':
            self.description = self.desc_box.text().zfill(4)
            if self.color_box != '':
                self.color = self.color_box.text().zfill(4)
            else:
                self.color = 'NONE'
            if self.size_box != '':
                self.size = self.size_box.text()
            else:
                self.size = 'NONE'
            self.confirmed = True
            self.close()
        else:
            pass

    def cancel_clicked(self):
        self.close()

class UPCPOWarningDialog(Ui_Dialog):
    def __init__(self, parent, item, inv_num, po_num, store):
        super(Ui_Dialog, self).__init__()
        self.parent = parent
        self.item = item
        self.confirmed = False
        self.setupUi(parent)
        self.populate_table(store)
        self.WarningLabel.setText("UPC %s (Style %s) on invoice# %s is not allocated to store# %s on PO# %s" %
                                  (item.upc, item.long_style, inv_num, store.store_num, po_num))
        self.IgnoreButton.clicked.connect(self.ignore_clicked)
        self.ConfirmButton.clicked.connect(self.confirm_clicked)
        self.CancelButton.clicked.connect(self.cancel_clicked)

    def populate_table(self, store):
        self.tableWidget.setHorizontalHeaderLabels(['Style', 'UPC', 'Cost', 'Qty'])
        row = 0
        self.tableWidget.setRowCount(len(store.items.values()))
        for item in store.items.values():
            self.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(item.style_num))
            self.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(item.upc))
            self.tableWidget.setItem(row, 2, QtWidgets.QTableWidgetItem('$' + str(item.cost)))
            self.tableWidget.setItem(row, 3, QtWidgets.QTableWidgetItem(str(item.total_qty)))
            row += 1

    def ignore_clicked(self):
        self.confirmed = True
        self.parent.close()

    def confirm_clicked(self):
        self.item.upc = self.tableWidget.selectedItems()[1].text()
        self.confirmed = True
        self.parent.close()

    def cancel_clicked(self):
        self.confirmed = False
        self.parent.close()

if __name__ == '__main__':
    x = QtWidgets.QApplication(sys.argv)
    d = QtWidgets.QDialog()
    i = Product("ABC")
    i.upc = "12345"
    s = Store("123")
    s.items["1"] = Item("12346")
    s.items["2"] = Item("23468")
    a = UPCPOWarningDialog(d, i, "5322", "932185", s)
    a.parent.show()
    x.exec_()
    print(a.item.upc)
