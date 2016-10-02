import sys
from datetime import datetime
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5 import QtCore
from src.ui.viewmodels.poprinter import POPrintModel
from src.models.models import Order, Store, Item

def create_test_order():
    test_order = Order(po_number="Test Order",
                       customer="Test Customer",
                       dept_number="TestD",
                       label="Testing",
                       status="Testing",
                       create_date=datetime.now(),
                       start_date=datetime.now(),
                       cancel_date=datetime.now())
    test_store_1 = Store(store_number="TS01",
                         dc_number="00TS")
    test_item_1 = Item(upc="1234TEST1234",
                       style="Test-1234",
                       cost=50.0,
                       retail=100.0,
                       qty=5)
    test_item_2 = Item(upc="1234TEST5678",
                       style="Test-72",
                       cost=250.0,
                       retail=500.0,
                       qty=1)
    test_store_1.items.append(test_item_1)
    test_store_1.items.append(test_item_2)
    test_store_1.total_cost = sum([item.cost for item in test_store_1.items])
    test_store_1.total_retail = sum([item.retail for item in test_store_1.items])
    test_store_1.total_qty = sum([item.qty for item in test_store_1.items])
    test_store_2 = Store(store_number="TS02",
                         dc_number="00TS")
    test_item_3 = Item(upc="1234TEST8910",
                       style="Test-46",
                       cost=1000.0,
                       retail=2000.0,
                       qty=2)
    test_store_2.items.append(test_item_3)
    test_store_2.total_cost = sum([item.cost for item in test_store_2.items])
    test_store_2.total_retail = sum([item.retail for item in test_store_2.items])
    test_store_2.total_qty = sum([item.qty for item in test_store_2.items])
    test_order.stores.append(test_store_1)
    test_order.stores.append(test_store_2)
    test_order.total_cost = sum([store.total_cost for store in test_order.stores])
    test_order.total_retail = sum([store.total_retail for store in test_order.stores])
    test_order.total_qty = sum([store.total_qty for store in test_order.stores])
    return test_order

def test_row_count():
    order = create_test_order()
    app = QApplication(sys.argv)
    view = POPrintModel(order, QDialog())
    assert view.rowCount() == 4

def test_column_count():
    order = create_test_order()
    app = QApplication(sys.argv)
    view = POPrintModel(order, QDialog())
    assert view.columnCount() == 5

def test_header_upc_col():
    order = create_test_order()
    app = QApplication(sys.argv)
    view = POPrintModel(order, QDialog())
    assert view.headerData(0, QtCore.Qt.Horizontal) == "UPC"

def test_header_style_col():
    order = create_test_order()
    app = QApplication(sys.argv)
    view = POPrintModel(order, QDialog())
    assert view.headerData(1, QtCore.Qt.Horizontal).value() == "Style"

def test_header_total_col():
    order = create_test_order()
    app = QApplication(sys.argv)
    view = POPrintModel(order, QDialog())
    assert view.headerData(2, QtCore.Qt.Horizontal).value() == "Total"

def test_header_store_col():
    order = create_test_order()
    app = QApplication(sys.argv)
    view = POPrintModel(order, QDialog())
    assert view.headerData(3, QtCore.Qt.Horizontal).value() == "TS01"

class Test_DataMethod(object):
    def test_data_origin(self):
        order = create_test_order()
        app = QApplication(sys.argv)
        dialog = QDialog()
        view = POPrintModel(order, dialog)
        index = view.index(0, 0)
        assert view.data(index).value() == "1234TEST1234"

    def test_data_col1_row0(self):
        order = create_test_order()
        app = QApplication(sys.argv)
        dialog = QDialog()
        view = POPrintModel(order, dialog)
        index = view.index(0, 1)
        assert view.data(index).value() == "Test-1234"

    def test_data_col3_row0(self):
        order = create_test_order()
        app = QApplication(sys.argv)
        dialog = QDialog()
        view = POPrintModel(order, dialog)
        index = view.index(0, 3)
        assert view.data(index).value() == 5

    def test_data_col3_row1(self):
        order = create_test_order()
        app = QApplication(sys.argv)
        dialog = QDialog()
        view = POPrintModel(order, dialog)
        index = view.index(1, 3)
        assert view.data(index).value() == ''