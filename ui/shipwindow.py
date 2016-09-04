from ui.pyuic.UiShippingWindow import Ui_MainWindow
from ui.settingsdialog import SettingsDialog
from translate.translator import OutputTranslator
from translate.translatetest import TranslatorUnitTest
from helpers.config import read_config
from helpers.analysis import ship_log_analyzer
from PyQt5 import QtCore, QtWidgets, QtGui
from datetime import datetime, timedelta
import threading
import re

class ProgressThread(threading.Thread):
    def __init__(self, text):
        threading.Thread.__init__(self)
        self.p = ProgressDialog(text)

    def start(self):
        self.p.show()

class ProgressDialog(QtWidgets.QDialog):
    def __init__(self, text):
        QtWidgets.QDialog.__init__(self)
        self.setWindowTitle("Processing")
        self.setWindowIcon(QtGui.QIcon("Resources\MBIcon.bmp"))
        self.layout = QtWidgets.QVBoxLayout(self)
        self.header = QtWidgets.QLabel(self)
        self.header.setText(text)
        self.header.setAlignment(QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.header)
        self.label = QtWidgets.QLabel(self)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.label)
        self.progress_bar = QtWidgets.QProgressBar(self)
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(17)
        self.progress_bar.setTextVisible(False)
        self.layout.addWidget(self.progress_bar)

    @QtCore.pyqtSlot(str, int)
    def update_progress(self, text, progress):
        self.setFocus()
        self.label.setText(text)
        self.progress_bar.setValue(progress)

class ShippingWindow(Ui_MainWindow):
    def __init__(self, main_window):
        super(ShippingWindow, self).__init__()
        self.parent = main_window
        self.setupUi(self.parent)
        self.ShiplogLookup.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.ShiplogLookup.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)
        self.ShiplogLookup.setSelectionMode(QtWidgets.QTableWidget.MultiSelection)
        self.ShipDate.setDate(QtCore.QDate.currentDate())
        self.parent.setWindowTitle("MB EDI Shipping")
        self.parent.setWindowIcon(QtGui.QIcon("Resources\MBIcon.bmp"))
        self.settings = read_config('Config.yaml')
        for customer in sorted(list(self.settings['Customer Settings'].keys())):
            self.CustomerBox.addItem(customer)
        self.actionSettings.triggered.connect(self.open_settings)
        self.actionExecute_Shipments.triggered.connect(self.execute_translator)
        self.EntryExecuteButton.clicked.connect(self.execute_translator)
        self.ShiplogLookupButton.clicked.connect(self.shiplog_lookup)
        self.ShiplogExecuteButton.clicked.connect(self.shiplog_execute)
        self.invoice_table_setup()
        self.self_test()

    def self_test(self):
        thread1 = ProgressThread("Running Self-Test")
        t = TranslatorUnitTest(self.settings)
        t.o.initiate_db()
        thread1.start()
        t.run()
        t.test()

    def invoice_table_setup(self):
        self.InvoiceTable.setHorizontalHeaderLabels(['Invoice #', 'PO #', 'Discount', 'Memo?'])
        self.new_invoice_row()
        self.InvoiceTable.currentItemChanged.connect(self.add_new_row)

    def add_new_row(self):
        try:
            if self.InvoiceTable.selectedIndexes()[-1].row() == self.InvoiceTable.rowCount() - 1:
                self.new_invoice_row()
        except IndexError:
            return

    def new_invoice_row(self):
        count = self.InvoiceTable.rowCount()
        self.InvoiceTable.setRowCount(count + 1)
        item = QtWidgets.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
        item.setCheckState(QtCore.Qt.Unchecked)
        self.InvoiceTable.setItem(count, 3, item)

    def shiplog_lookup(self):
        date = self.ShipDate.date().toString("yyyyMMdd")
        array = []
        with open(self.settings['File Paths']['Shipping Log'], 'r') as shiplog:
            for line in shiplog:
                line = line.replace('"','').split(',')
                if line[0] == date:
                    array.append([line[1], line[10], line[11]])
        self.ShiplogLookup.setRowCount(len(array))
        for row in range(len(array)):
            for col in range(3):
                self.ShiplogLookup.setItem(row, col, QtWidgets.QTableWidgetItem(array[row][col]))
        an_array = [[array.index(item), item] for item in array]
        analysis = ship_log_analyzer(an_array, self.CustomerBox.currentText())
        for item in analysis:
            self.ShiplogLookup.selectRow(item[0])

    def shiplog_execute(self):
        items = self.ShiplogLookup.selectedItems()
        array = []
        for num in range((len(items) + 2) // 3):
            array.append([re.search(r'[0-9]+', items[num * 3 + 1].text()).group(0),
                          re.search(r'[0-9]+', items[num * 3 + 2].text()).group(0), 0, False])
        print(array)
        thread1 = ProgressThread("Processing")
        o = OutputTranslator(self.CustomerBox.currentText(), self.settings)
        o.get_customer_settings()
        o.initiate_db()
        thread1.start()
        if o.run(array):
            o.write_output()

    def execute_translator(self):
        thread1 = ProgressThread("Processing")
        t = TranslatorUnitTest(self.settings)
        o = OutputTranslator(self.CustomerBox.currentText(), self.settings)
        o.get_customer_settings()
        o.initiate_db()
        array = []
        for row in range(self.InvoiceTable.rowCount()):
            if self.InvoiceTable.item(row, 0) != None and self.InvoiceTable.item(row, 0) != '':
                row_array = []
                for column in range(self.InvoiceTable.columnCount()):
                    if column == 2:
                        try:
                            row_array.append(int(self.InvoiceTable.item(row, column).data(QtCore.Qt.DisplayRole)))
                        except (ValueError, AttributeError):
                            row_array.append(0)
                    elif column < 3:
                        try:
                            row_array.append(str(self.InvoiceTable.item(row, column).data(QtCore.Qt.DisplayRole)))
                        except AttributeError:
                            row_array.append(0)
                    else:
                        row_array.append(self.InvoiceTable.item(row, column).checkState())
                array.append(row_array)
        thread1.start()
        if o.run(array):
            o.write_output()

    def open_settings(self):
        print("Settings")
        q = QtWidgets.QDialog()
        settings_window = SettingsDialog(q, self.settings)
        q.exec_()
        self.settings = settings_window.settings
        item_list = [self.CustomerBox.itemText(i) for i in range(self.CustomerBox.count())]
        for customer in self.settings['Customer Settings'].keys():
            if not customer in item_list:
                self.CustomerBox.addItem(customer)