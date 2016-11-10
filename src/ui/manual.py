from src.ui.pyuic.UiManualInvoiceDialog import Ui_ManualDialog
from src.translate.translator import OutputTranslator, generate_sscc
from src.models.models import Invoice, Item
from PyQt5 import QtCore, QtGui

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
        for store in sorted(self.order.stores, key=lambda store: store.store_number):
            self.StoreBox.addItem(store.store_number)
        self.StoreBox.setCurrentText(self.order.customer)
        self.StoreBox.activated.connect(self.populate_items)
        self.ExecuteButton.clicked.connect(self.both_clicked)

    def populate_items(self):
        store = next((st for st in self.order.stores if st.store_number == self.StoreBox.currentText()))
        self.ItemTable.model().item_list = sorted(store.items, key=lambda i: i.style)
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
        invoice = Invoice(invoice_number=self.InvoiceEdit.text(),
                          customer=self.CustomerBox.currentText(),
                          po_number=self.order.po_number,
                          dc_number=self.DcBox.text(),
                          tracking_number=self.TrackingBox.text(),
                          ship_date=self.ShipDateCal.date(),
                          store_number=self.StoreBox.currentText())
        invoice.dept_number(False, self.settings['Customer Settings']
                            [invoice.customer]['Asset Department'],
                            self.settings['Customer Settings']
                            [invoice.customer]['Memo Department'])
        invoice.discount(self.DiscountSpin.value())
        invoice.items = self.ItemTable.model().item_list
        invoice.get_totals()
        invoice.sscc_number = generate_sscc(invoice.invoice_number)
        return invoice


class ItemModel(QtCore.QAbstractTableModel):
    def __init__(self, parent, *args):
        QtCore.QAbstractTableModel.__init__(self, parent, *args)
        self.item_list = []
        self.attr = ['upc', 'style', 'cost', 'qty']
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
