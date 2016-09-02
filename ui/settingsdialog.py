from ui.pyuic.UiSettingsDialog import Ui_SettingsDialog
from ui.pyuic.UiCustomerAddDialog import Ui_CustomerAddDialog
from PyQt5 import QtCore, QtWidgets, QtGui
import yaml

class CustomerModel(QtCore.QAbstractTableModel):
    def __init__(self, customer_list, parent, *args):
        QtCore.QAbstractTableModel.__init__(self, parent, *args)
        self.customers = list(customer_list.values())
        self.view_attr = ['name', 'inv_edi_id', 'ship_edi_id']
        self.headers = list(self.customers[0].keys())

    def flags(self, index):
        return QtCore.QAbstractTableModel.flags(self, index) | QtCore.Qt.ItemIsEditable

    def rowCount(self, parent = QtCore.QModelIndex()):
        return len(self.customers)
        
    def columnCount(self, parent = QtCore.QModelIndex()):
        return len(self.headers)

    def headerData(self, section, Orientation, role = QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.DisplayRole and Orientation == QtCore.Qt.Horizontal:
            return self.headers[section]
        return QtCore.QAbstractTableModel.headerData(self, section, Orientation, role)

    def data(self, index, role = QtCore.Qt.DisplayRole):
        if not index.isValid():
            return QtCore.QVariant()
        elif role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()
        else:
            return QtCore.QVariant(self.customers[index.row()][self.headers[index.column()]])

    def setData(self, index, data, role = QtCore.Qt.EditRole):
        if index.isValid():
            self.customers[index.row()][self.headers[index.column()]] = data
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
        self.model = CustomerModel(self.settings['Customer Settings'], self.parent)
        self.CustomerTable.setModel(self.model)
        self.populate_fields()
        self.populate_list()

    def write_config(self, config_file):
        with open(config_file, 'w') as config:
            yaml.dump(self.settings, config, default_flow_style=False)

    def populate_fields(self):
        self.ShipLogLine.setText(self.settings['File Paths']['Shipping Log'])
        self.DestLogLine.setText(self.settings['File Paths']['Destination Log'])
        self.DescLogLine.setText(self.settings['File Paths']['Description Log'])
        self.UPCExceptLine.setText(self.settings['File Paths']['UPC Exception Log'])
        self.LabelRecordLine.setText(self.settings['File Paths']['Label Record File'])
        self.MapdataLine.setText(self.settings['File Paths']['MAPDATA Path'])
        self.POdataLine.setText(self.settings['File Paths']['PO Database File'])
        self.ConnLine.setText(self.settings['SQL Settings']['Connection String'])
        self.InvQueryLine.setText(self.settings['SQL Settings']['Invoice Query'])
        self.DestQueryLine.setText(self.settings['SQL Settings']['Destination Query'])
        self.MemDestQueryLine.setText(self.settings['SQL Settings']['Memo Destination Query'])
        self.UPCQueryLine.setText(self.settings['SQL Settings']['UPC Query'])
        self.RingUPCQueryLine.setText(self.settings['SQL Settings']['Ring UPC Query'])

    def populate_list(self):
        self.StatusList.setRowCount(len(self.settings['Statuses']) + 5)
        for num in range(len(self.settings['Statuses'])):
            self.StatusList.setItem(num, 0, QtWidgets.QTableWidgetItem(self.settings['Statuses'][num]))

    def add_new_clicked(self):
        q = QtWidgets.QDialog()
        add_window = Ui_CustomerAddDialog()
        add_window.setupUi(q, list(self.settings["Customer Settings"].values())[0])
        q.exec_()
        if add_window.confirmed == True and add_window.customer != '':
            self.settings['Customer Settings'][add_window.customer["Name"]] = add_window.customer
            self.CustomerTable.model().layoutChanged.emit()

    def delete_clicked(self):
        print(self.settings['Customer Settings'])
        print(self.CustomerTable.model().customers)
        print(self.CustomerTable.selectedIndexes()[0].row())
        del self.settings['Customer Settings'][self.CustomerTable.model().customers[self.CustomerTable.selectedIndexes()[0].row()]['Name']]   
        self.CustomerTable.model().layoutChanged.emit()
        
    def accept_clicked(self):
        self.settings['File Paths']['Shipping Log'] = self.ShipLogLine.text()
        self.settings['File Paths']['Destination Log'] = self.DestLogLine.text()
        self.settings['File Paths']['Description Log'] = self.DescLogLine.text()
        self.settings['File Paths']['UPC Exception Log'] = self.UPCExceptLine.text()
        self.settings['File Paths']['Label Record File'] = self.LabelRecordLine.text()
        self.settings['File Paths']['MAPDATA Path'] = self.MapdataLine.text()
        self.settings['File Paths']['PO Database File'] = self.POdataLine.text()
        self.settings['SQL Settings']['Connection String'] = self.ConnLine.text()
        self.settings['SQL Settings']['Invoice Query'] = self.InvQueryLine.text()
        self.settings['SQL Settings']['Destination Query'] = self.DestQueryLine.text()
        self.settings['SQL Settings']['Memo Destination Query'] = self.MemDestQueryLine.text()
        self.settings['SQL Settings']['UPC Query'] = self.UPCQueryLine.text()
        self.settings['SQL Settings']['Ring UPC Query'] = self.RingUPCQueryLine.text()
        self.settings['SQL Settings']['CustomerSettings'] = self.CustomerTable.model().customers
        self.settings['Statuses'] = []
        for num in range(self.StatusList.rowCount()):
            if self.StatusList.item(num, 0) != None:
                self.settings['Statuses'].append(self.StatusList.item(num, 0).text())
        self.write_config('Config.yaml')
        self.parent.close()
    
    def cancel_clicked(self):
        self.parent.close()