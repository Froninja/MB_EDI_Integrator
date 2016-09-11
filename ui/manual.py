from ui.pyuic.UiManualInvoiceDialog import Ui_ManualDialog
from translate.translator import OutputTranslator
from models.invoice import Invoice, Product
from PyQt5 import QtCore

class ManualInvoiceWindow(Ui_ManualDialog):
    def __init__(self, main_window, settings, order):
        super(ManualInvoiceWindow, self).__init__()
        self.setupUi(main_window)
        main_window.setWindowTitle("Data Entry")
        main_window.setWindowIcon(QtGui.QIcon("Resources\\MBIcon.bmp"))
        self.settings = settings
        self.order = order
        self.ItemTable.setModel(ItemModel(main_window))
        self.ShipDateCal.setDate(QtCore.QDate.currentDate())
        for customer in sorted(list(self.settings['Customer Settings'].keys())):
            self.CustomerBox.addItem(customer)
        for store in sorted(list(self.order.stores.keys())):
            self.StoreBox.addItem(store)
        self.StoreBox.setCurrentText(self.order.customer)
        self.StoreBox.activated.connect(self.populate_items)
        self.BothButton.clicked.connect(self.both_clicked)

    def populate_items(self):
        store = self.order.stores[self.StoreBox.currentText()]
        self.ItemTable.model().item_list = sorted(store.items.values(), key=lambda i: i.style_num)
        self.ItemTable.model().layoutChanged.emit()

    def both_clicked(self):
        output = OutputTranslator(self.CustomerBox.currentText(), self.settings)
        output.invoice_list = [self.generate_invoice()]
        output.get_customer_settings()
        output.get_validater()
        if not output.validater.check_po():
            return
        output.write_output()

    def generate_invoice(self):
        invoice = Invoice(self.InvoiceEdit.text())
        invoice.purchase_order_number = self.order.po_number
        invoice.customer = self.CustomerBox.currentText()
        invoice.get_dept_num(False, self.settings['Customer Settings']
                             [invoice.customer]['Asset Department'],
                             self.settings['Customer Settings']
                             [invoice.customer]['Memo Department'])
        invoice.tracking_number = self.TrackingBox.text()
        invoice.discount(self.DiscountSpin.value())
        invoice.ship_date = self.ShipDateCal.date()
        invoice.store_number = self.StoreBox.currentText()
        invoice.items = [Product.from_item(item) for item in self.ItemTable.model().item_list]
        invoice.totals()
        invoice.get_sscc()
        return invoice


class ItemModel(QtCore.QAbstractTableModel):
    def __init__(self, parent, *args):
        QtCore.QAbstractTableModel.__init__(self, parent, *args)
        self.item_list = []
        self.attr = ['upc', 'style_num', 'cost', 'total_qty']
        self.headers = ['UPC', 'Style Number', 'Cost', 'Qty']

    def flags(self, index):
        if index.isValid() and index.column() == 3:
            return super().flags(index) | QtCore.Qt.ItemIsEditable
        else:
            return super().flags(index)

    def rowCount(self, parent = QtCore.QModelIndex()):
        return len(self.item_list)

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
            return QtCore.QVariant(getattr(self.item_list[index.row()], self.attr[index.column()]))

    def setData(self, index, value, role = QtCore.Qt.EditRole):
        if index.isValid() and role == QtCore.Qt.EditRole:
            setattr(self.item_list[index.row()], self.attr[index.column()], value)
            return True
