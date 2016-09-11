from src.models.purchaseorder import PurchaseOrder, Store, Item
from PyQt5 import QtCore, QtWidgets, QtGui
from datetime import datetime
import operator

class POModel(QtCore.QAbstractTableModel):
    def __init__(self, po_list, parent, mainform, *args):
        QtCore.QAbstractTableModel.__init__(self, parent, *args)
        self.po_list = po_list
        self.mainform = mainform
        self.attr = ['customer', 'po_number', 'label', 'status', 'dept', 'total_cost', 'shipped_cost',
                     'start_ship', 'cancel_ship', 'creation_date']
        self.headers = ['Customer', 'PO#', 'Label', 'Status', 'Department', 'Total Cost', 'Shipped Cost',
                        'Start Date', 'Cancel Date', 'Create Date']

    def flags(self, index):
        if index.isValid() and index.column() in [2,3]:
            return super().flags(index) | QtCore.Qt.ItemIsEditable
        elif index.isValid() and self.parent_form.EditAllCheck.checkState() == QtCore.Qt.Checked \
            and index.column() != 1:
            return super().flags(index) | QtCore.Qt.ItemIsEditable
        else:
            return super().flags(index)

    def rowCount(self, parent = QtCore.QModelIndex()):
        return len(self.po_list)

    def columnCount(self, parent = QtCore.QModelIndex()):
        return len(self.headers)

    def headerData(self, int, Orientation, role = QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.DisplayRole and Orientation == QtCore.Qt.Horizontal:
            return QtCore.QVariant(self.headers[int])
        return QtCore.QAbstractTableModel.headerData(self, int, Orientation, role)

    def data(self, index, role = QtCore.Qt.DisplayRole):
        if not index.isValid():
            return QtCore.QVariant()
        elif role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()
        else:
            try:
                return QtCore.QVariant(getattr(self.po_list[index.row()], self.attr[index.column()]).strftime("%m/%d/%Y"))
            except AttributeError:
                return QtCore.QVariant(getattr(self.po_list[index.row()], self.attr[index.column()]))

    def setData(self, index, value, role = QtCore.Qt.EditRole):
        print("Calling with %s" % value)
        if index.isValid() and role == QtCore.Qt.EditRole:
            po = self.po_list[index.row()]
            if index.column() >= len(self.attr) - 3:
                try:
                    setattr(po, self.attr[index.column()], datetime.strptime(value, "%m/%d/%Y"))
                    print("Value is good")
                    self.mainform.po_db.update(po)
                except ValueError:
                    print("Invalid date format")
            else:
                setattr(po, self.attr[index.column()], value)
                self.mainform.po_db.update(po)
            return True

    def sort(self, int, order = QtCore.Qt.AscendingOrder):
        self.layoutAboutToBeChanged.emit()
        if order != QtCore.Qt.DescendingOrder:
            self.po_list.sort(key=operator.attrgetter(self.attr[int]), reverse=True)
        else:
            self.po_list.sort(key=operator.attrgetter(self.attr[int]))
        self.layoutChanged.emit()