from UiSettingsDialog import Ui_SettingsDialog
from CustomerSettings import CustomerSettings
from UiCustomerAddDialog import Ui_CustomerAddDialog
from PyQt5 import QtCore, QtWidgets, QtGui

class CustomerModel(QtCore.QAbstractTableModel):
    def __init__(self, customer_list, parent, *args):
        QtCore.QAbstractTableModel.__init__(self, parent, *args)
        self.customers = customer_list
        self.view_attr = ['name', 'inv_edi_id', 'ship_edi_id']
        self.headers = CustomerSettings().sorted_dict()

    def flags(self, index):
        return QtCore.QAbstractTableModel.flags(self, index) | QtCore.Qt.ItemIsEditable

    def rowCount(self, parent = QtCore.QModelIndex()):
        return len(self.customers)
        
    def columnCount(self, parent = QtCore.QModelIndex()):
        return len(self.headers)

    def headerData(self, section, Orientation, role = QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.DisplayRole and Orientation == QtCore.Qt.Horizontal:
            return self.headers[section][2:].replace('_',' ').title()
        return QtCore.QAbstractTableModel.headerData(self, section, Orientation, role)

    def data(self, index, role = QtCore.Qt.DisplayRole):
        if not index.isValid():
            return QtCore.QVariant()
        elif role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()
        else:
            return QtCore.QVariant(getattr(self.customers[index.row()], CustomerSettings().sorted_dict()[index.column()]))

    def setData(self, index, data, role = QtCore.Qt.EditRole):
        if index.isValid():
            setattr(self.customers[index.row()], CustomerSettings().sorted_dict()[index.column()], data)
            return True
        else:
            return False

class SettingsDialog(Ui_SettingsDialog):
    def __init__(self, settings_dialog, settings):
        super(SettingsDialog, self).__init__()
        self.parent = settings_dialog
        self.parent.setWindowIcon(QtGui.QIcon("Resources\MBIcon.bmp"))
        self.setupUi(self.parent)
        self.CancelButton.clicked.connect(self.cancel_clicked)
        self.AcceptButton.clicked.connect(self.accept_clicked)
        self.AddCustomerButton.clicked.connect(self.add_new_clicked)
        self.DeleteCustomerButton.clicked.connect(self.delete_clicked)
        self.settings = settings
        self.model = CustomerModel(self.settings['customers'], self.parent)
        self.CustomerTable.setModel(self.model)
        self.populate_fields()
        self.populate_list()

    def write_config(self, config_file):
        output = ''
        with open(config_file, 'w') as config:
            output += "Required File Paths:\n"
            output += "Shipping Log: %s\n" % self.settings['shiplog']
            output += "Destination Log: %s\n" % self.settings['destlog']
            output += "Description Log: %s\n" % self.settings['desclog']
            output += "UPC Exception Log: %s\n" % self.settings['upcexceptlog']
            output += "Label Record File: %s\n" % self.settings['outputlog']
            output += "MAPDATA Path: %s\n" % self.settings['mapdata']
            output += "PO Database File: %s\n" % self.settings['po_db']
            output += "\nSQL Settings:\n"
            output += "Connection String: %s\n" % self.settings['connstring']
            output += "Invoice Query: %s\n" % self.settings['invquery']
            output += "Destination Query: %s\n" % self.settings['destquery']
            output += "Memo Destination Query: %s\n" % self.settings['memodestquery']
            output += "UPC Query: %s\n" % self.settings['upcquery']
            output += "Ring UPC Query: %s\n" % self.settings['ringupcquery']
            output += "\nStatus Options: %s" % ','.join(self.settings['status'])
            output += "\nCustomer Settings:\n"
            for customer in self.settings['customers']:
                output += "Customer: "
                for setting in customer.sorted_dict():
                    output += "%s>>" % getattr(customer, setting)
                output += "\n"
            config.write(output)

    def populate_fields(self):
        self.ShipLogLine.setText(self.settings['shiplog'])
        self.DestLogLine.setText(self.settings['destlog'])
        self.DescLogLine.setText(self.settings['desclog'])
        self.UPCExceptLine.setText(self.settings['upcexceptlog'])
        self.LabelRecordLine.setText(self.settings['outputlog'])
        self.MapdataLine.setText(self.settings['mapdata'])
        self.POdataLine.setText(self.settings['po_db'])
        self.ConnLine.setText(self.settings['connstring'])
        self.InvQueryLine.setText(self.settings['invquery'])
        self.DestQueryLine.setText(self.settings['destquery'])
        self.MemDestQueryLine.setText(self.settings['memodestquery'])
        self.UPCQueryLine.setText(self.settings['upcquery'])
        self.RingUPCQueryLine.setText(self.settings['ringupcquery'])

    def populate_list(self):
        self.StatusList.setRowCount(len(self.settings['status']) + 5)
        for num in range(len(self.settings['status'])):
            self.StatusList.setItem(num, 0, QtWidgets.QTableWidgetItem(self.settings['status'][num]))

    def add_new_clicked(self):
        q = QtWidgets.QDialog()
        add_window = Ui_CustomerAddDialog()
        add_window.setupUi(q)
        q.exec_()
        if add_window.confirmed == True and add_window.customer != '':
            self.settings['customers'].append(add_window.customer)
            self.CustomerTable.model().layoutChanged.emit()

    def delete_clicked(self):
        self.settings['customers'].remove(self.CustomerTable.model().customers[self.CustomerTable.selectedIndexes()[0].row()])        
        self.CustomerTable.model().layoutChanged.emit()
        
    def accept_clicked(self):
        self.settings['shiplog'] = self.ShipLogLine.text()
        self.settings['destlog'] = self.DestLogLine.text()
        self.settings['desclog'] = self.DescLogLine.text()
        self.settings['upcexceptlog'] = self.UPCExceptLine.text()
        self.settings['outputlog'] = self.LabelRecordLine.text()
        self.settings['mapdata'] = self.MapdataLine.text()
        self.settings['po_db'] = self.POdataLine.text()
        self.settings['connstring'] = self.ConnLine.text()
        self.settings['invquery'] = self.InvQueryLine.text()
        self.settings['destquery'] = self.DestQueryLine.text()
        self.settings['memodestquery'] = self.MemDestQueryLine.text()
        self.settings['upcquery'] = self.UPCQueryLine.text()
        self.settings['ringupcquery'] = self.RingUPCQueryLine.text()
        self.settings['customers'] = self.CustomerTable.model().customers
        self.settings['status'] = []
        for num in range(self.StatusList.rowCount()):
            if self.StatusList.item(num, 0) != None:
                self.settings['status'].append(self.StatusList.item(num, 0).text())
        self.write_config('Config.txt')
        self.parent.close()
    
    def cancel_clicked(self):
        self.parent.close()