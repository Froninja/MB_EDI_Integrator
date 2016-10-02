from PyQt5 import QtCore, QtGui, QtWidgets, QtPrintSupport

class POPrintModel(QtCore.QAbstractTableModel):
    def __init__(self, po, parent, *args):
        QtCore.QAbstractTableModel.__init__(self, parent, *args)
        self.po = po
        self.store_list = sorted(self.po.stores, key=lambda store: store.store_number)
        self.item_list = []
        for store in self.store_list:
            for item in store.items:
                if item.upc not in [item.upc for item in self.item_list]:
                    self.item_list.append(item)
        self.item_list.sort(key=lambda item: item.style)

    def rowCount(self, parent = QtCore.QModelIndex()):
        return len(self.item_list) + 1

    def columnCount(self, parent = QtCore.QModelIndex()):
        return len(self.po.stores) + 3

    def headerData(self, int, orientation, role = QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.DisplayRole and orientation == QtCore.Qt.Horizontal:
            if int == 0:
                return QtCore.QVariant("UPC")
            elif int == 1:
                return QtCore.QVariant("Style")
            elif int == 2:
                return QtCore.QVariant("Total")
            else:
                return QtCore.QVariant(self.store_list[int - 3].store_number)
        return QtCore.QAbstractTableModel.headerData(self, int, orientation, role)

    def data(self, index, role = QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.DisplayRole:
            if index.row() == len(self.item_list):
                if index.column() < 1:
                    return QtCore.QVariant('')
                elif index.column() == 1:
                    return QtCore.QVariant('Total')
                elif index.column() == 2:
                    i_list = []
                    for store in self.store_list:
                        i_list += [item for item in store.items]
                    return QtCore.QVariant(sum([item.qty for item in i_list]))
                else:                    
                    store = self.store_list[index.column() - 3]
                    return QtCore.QVariant(sum([item.qty for item in store.items]))
            elif index.column() == 0:
                return QtCore.QVariant(self.item_list[index.row()].upc)
            elif index.column() == 1:
                return QtCore.QVariant(self.item_list[index.row()].style)
            elif index.column() == 2:
                i_list = []
                for store in self.store_list:
                    i_list += [item for item in store.items]
                upc = self.item_list[index.row()].upc       
                return QtCore.QVariant(sum([item.qty for item in i_list if item.upc == upc]))
            else:
                item = self.item_list[index.row()]
                store = self.store_list[index.column() - 3]
                if item in store.items:
                    return QtCore.QVariant(item.qty)
                else:
                    return QtCore.QVariant('')

    def sort(self, int, order = QtCore.Qt.AscendingOrder):
        self.layoutAboutToBeChanged.emit()
        if order != QtCore.Qt.DescendingOrder and int == 0:
            self.item_list.sort(key=lambda item: item.upc, reverse=True)
        elif int == 0:
            self.item_list.sort(key=lambda item: item.upc)
        elif order != QtCore.Qt.DescendingOrder and int == 1:
            self.item_list.sort(key=lambda item: item.style, reverse=True)
        elif int == 1:
            self.item_list.sort(key=lambda item: item.style)
        self.layoutChanged.emit()

class Ui_POPrintView(object):
    def setupUi(self, po_list, POPrintView):
        POPrintView.setObjectName("POPrintView")
        POPrintView.setWindowTitle("MB EDI PO# %s" % po_list[0].po_number)
        POPrintView.setWindowIcon(QtGui.QIcon("Resources\\MBIcon.bmp"))
        self.parent = POPrintView
        self.po_list = po_list
        self.gridLayout = QtWidgets.QGridLayout(POPrintView)
        self.gridLayout.setObjectName("gridLayout")
        self.tables = []
        index = 0
        for po in self.po_list:
            po_table = QtWidgets.QTableView()
            po_model = POPrintModel(po, self.parent)
            po_table.setModel(po_model)
            po_table.setSortingEnabled(True)
            self.gridLayout.addWidget(po_table, index, 0)
            self.tables.append(po_table)
            index += 1
        self.confirmButton = QtWidgets.QPushButton(POPrintView)
        self.confirmButton.setObjectName("Preview")
        self.confirmButton.setText("Preview")
        self.confirmButton.clicked.connect(self.handlePreview)
        self.gridLayout.addWidget(self.confirmButton, index, 0)

    def handlePrint(self):
        dialog = QtPrintSupport.QPrintDialog()
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            self.handlePaintRequest(dialog.printer())

    def handlePreview(self):
        dialog = QtPrintSupport.QPrintPreviewDialog()
        dialog.paintRequested.connect(self.handlePaintRequest)
        dialog.exec_()

    def handlePaintRequest(self, printer):
        document = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(document)
        model = self.tables[0].model()
        cursor.insertText("PO# " + self.po_list[0].po_number + '\n')
        table = cursor.insertTable(
            model.rowCount() + 1, model.columnCount())
        index = 0
        for row in range(table.rows()):
            for column in range(table.columns()):
                if row == 0:
                    cursor.insertText(model.headerData(column, QtCore.Qt.Horizontal).value())
                    cursor.movePosition(QtGui.QTextCursor.NextCell)
                else:
                    cursor.insertText(str(model.index(row - 1, column).data()))
                    cursor.movePosition(QtGui.QTextCursor.NextCell)
        document.print_(printer)