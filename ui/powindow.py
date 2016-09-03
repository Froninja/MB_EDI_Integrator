from ui.pyuic.UiPOWindow import Ui_MainWindow
from ui.settingsdialog import SettingsDialog
from ui.storeview import StoreViewWindow
from db.podb import PurchaseOrderDB
from ui.viewmodels.pomodel import POModel
from ui.viewmodels.poprinter import Ui_POPrintView
from helpers.export import Exporter
from helpers.config import read_config
from PyQt5 import QtCore, QtWidgets, QtGui, QtPrintSupport
from datetime import datetime, timedelta
from contextlib import redirect_stdout

class TableComboBox(QtWidgets.QComboBox):
    def __init__(self, model, index):
        super(QtWidgets.QComboBox, self).__init__()

        self.activated.connect(lambda: model.setData(index, self.currentText()))

    def currentData(self, role = QtCore.Qt.UserRole):
        return super().currentData()


class POWindow(Ui_MainWindow):
    def __init__(self, main_window):
        super(POWindow, self).__init__()
        self.parent = main_window
        self.setupUi(self.parent)
        main_window.setWindowTitle("MB EDI Purchase Orders")
        main_window.setWindowIcon(QtGui.QIcon("Resources\MBIcon.bmp"))
        self.settings = read_config('Config.yaml')
        self.create_filter_boxes()
        for customer in sorted(list(self.settings['Customer Settings'].keys())):
            self.CustomerBox.addItem(customer)
        self.actionSettings.triggered.connect(self.open_settings)
        self.actionExport_as_Spreadsheet.triggered.connect(self.export_for_ss)
        self.actionView_Distro.triggered.connect(self.open_po_table_view)
        self.CustomerBox.activated.connect(self.po_list_filter)
        self.AgeSlider.valueChanged.connect(self.po_list_filter)
        self.po_db = PurchaseOrderDB(self.settings)
        self.po_model = POModel(self.po_db.queryall(), self.parent, self)
        self.po_model.parent_form = self
        self.po_model.layoutChanged.connect(self.insert_combo_boxes)
        self.POTable.setModel(self.po_model)
        self.POTable.doubleClicked.connect(self.open_store_view)
        self.create_context_actions()
        self.insert_combo_boxes()
        self.POTable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

    def create_context_actions(self):
        self.POTable.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        print_action = QtWidgets.QAction("Print", self.POTable)
        print_action.triggered.connect(self.print_po)
        self.POTable.addAction(print_action)
        distro_action = QtWidgets.QAction("View as Table", self.POTable)
        distro_action.triggered.connect(self.open_po_table_view)
        self.POTable.addAction(distro_action)

    def create_filter_boxes(self):
        self.status_boxes = []
        for status in self.settings['Statuses']:
            c = QtWidgets.QCheckBox(status, self.FilterFrame)
            c.clicked.connect(self.po_list_filter)
            self.FilterFrame.layout().addWidget(c)
            self.status_boxes.append(c)

    def insert_combo_boxes(self):
        for row in range(self.POTable.model().rowCount()):
            i = self.POTable.model().index(row, 3)
            c = TableComboBox(self.POTable.model(), i)
            options = [''] + self.settings['Statuses']
            c.addItems(options)
            try:
                c.setCurrentIndex(options.index(self.POTable.model().po_list[i.row()].status))
            except:
                pass
            self.POTable.setIndexWidget(i, c)
        
    def po_list_filter(self):
        customer = self.CustomerBox.currentText()
        po_list = []
        counter = 0
        tdiff = (self.AgeSlider.value() * 30) + 30
        self.DaysLabel.setText(str(tdiff))
        status = []
        for num in range(len(self.status_boxes)):
            if self.status_boxes[num].isChecked() == True:
                status.append(self.settings['Statuses'][num])
        self.po_model.po_list = self.po_db.queryfilters(customer, tdiff, status)
        self.po_model.resetInternalData()
        self.POTable.model().modelReset.emit()
        self.insert_combo_boxes()

    def open_store_view(self):
        po = self.POTable.model().po_list[self.POTable.selectedIndexes()[0].row()]
        q = QtWidgets.QMainWindow()
        self.store_window = StoreViewWindow(q, po)
        q.show()

    def open_po_table_view(self):
        po_list = []
        for index in self.POTable.selectedIndexes():
            po_list.append(self.POTable.model().po_list[index.row()])
        q = QtWidgets.QDialog()
        self.po_view = Ui_POPrintView()
        self.po_view.setupUi(po_list, q)
        q.exec_()
        
    def export_for_ss(self):
        indices = self.POTable.selectedIndexes()
        po_list = []
        for index in indices:
            po_list.append(self.po_model.po_list[index.row()])
        print(po_list)
        exporter = Exporter()
        exporter.set_po_list(po_list)
        exporter.export_spreadsheet('Export.xls')

    def open_settings(self):
        q = QtWidgets.QDialog()
        settings_window = SettingsDialog(q, self.settings)
        q.exec_()
        self.settings = settings_window.settings
        item_list = [self.CustomerBox.itemText(i) for i in range(self.CustomerBox.count())]
        for customer in self.settings['Customer Settings'].keys():
            if not customer in item_list:
                self.CustomerBox.addItem(customer)

    def print_po(self):
        po = self.POTable.model().po_list[self.POTable.selectedIndexes()[0].row()]
        printer = POPrinter(po, self.parent)

class POPrinter(QtCore.QObject):
    def __init__(self, po, parent):
        QtCore.QObject.__init__(self)
        self.po = po
        #self.handlePrint(parent)
        self.print_po()

    def print_po(self):
        dialog = QtPrintSupport.QPrintPreviewDialog()
        dialog.paintRequested.connect(self.paint_po)
        dialog.exec_()

    def handlePrint(self, parent):
        print("Handling print")
        printer = QtPrintSupport.QPrinter()
        #printer.setOutputFileName("")
        self.dialog = QtPrintSupport.QPrintDialog(printer, parent)
        print(self.dialog)
        if self.dialog.exec_() == QtWidgets.QDialog.Accepted:
            print(self.dialog.printer())
            self.paint_po(self.dialog.printer())

    def paint_po(self, printer):
        document = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(document)
        header_block = QtGui.QTextBlockFormat()
        header_block.setAlignment(QtCore.Qt.AlignHCenter)

        header_text = QtGui.QTextCharFormat()
        header_text.setFontPointSize(24)

        info_block = QtGui.QTextBlockFormat()
        info_block.setAlignment(QtCore.Qt.AlignHCenter)

        info_text = QtGui.QTextCharFormat()
        info_text.setFontPointSize(15)

        style_block = QtGui.QTextBlockFormat()

        style_text = QtGui.QTextCharFormat()
        style_text.setFontPointSize(13)

        cursor.insertBlock(header_block)
        cursor.setCharFormat(header_text)
        cursor.insertText("%s\nPO# %s\n" % (self.po.customer, self.po.po_number))
        cursor.movePosition(QtGui.QTextCursor.NextBlock)

        cursor.insertBlock(info_block)
        cursor.setCharFormat(info_text)
        cursor.insertText("Start Ship Date: %s\tCancel Date: %s" % (self.po.start_ship.strftime("%m/%d/%Y")
                                                                      , self.po.cancel_ship.strftime("%m/%d/%Y")))
        cursor.movePosition(QtGui.QTextCursor.NextBlock)

        cursor.insertBlock(info_block)
        cursor.insertText("Department: %s\t\tDiscount Required: %s\n" % (self.po.dept, self.po.discount))
        cursor.movePosition(QtGui.QTextCursor.NextBlock)

        cursor.insertBlock(header_block)
        cursor.insertText("Stores")
        for store in sorted(self.po.stores.values(), key=lambda store: store.store_num):
            cursor.insertBlock(style_block)
            cursor.setCharFormat(style_text)
            cursor.insertText("Store#: %s\tTotal Cost Value: $%s\t Total Qty: %s\n" % (store.store_num,
                                                                                     sum([item.cost * item.total_qty for item in store.items.values()]),
                                                                                     sum([item.total_qty for item in store.items.values()])))
            cursor.insertText("Items\n")
            for item in sorted(store.items.values(), key=lambda item: item.style_num):
                cursor.insertText("Style: %s\tUPC: %s\tUnit Cost: $%s\tQty: %s\n" % (item.style_num, item.UPC,
                                                                                   item.cost, item.total_qty))

        document.print_(printer)