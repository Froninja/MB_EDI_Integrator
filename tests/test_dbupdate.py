from datetime import datetime
from src.db.dbupdate import *
from src.models.models import Order, Store, Item

def mock_row():
    return [
        "TestClient",
        "TestPO",
        "10/31/2016",
        "11/11/2016",
        "TestStore",
        "TestUpc",
        "TestStyle",
        500.0,
        1200.0,
        5,
        "2016/10/13",
        "TestDept"
    ]

def mock_settings():
    return {
        'Customer Settings': {
            'TestCustomer': {
                'Name': 'TestCustomer',
                'PO ID': 'TestClient'
                }
            }
        }

def test_create_item():
    test_item = Item(upc="TestUpc",
                     style="TestStyle",
                     cost=500.0,
                     retail=1200.0,
                     qty=5)
    assert create_item(mock_row()).__repr__() == test_item.__repr__()

def test_create_store():
    test_store = Store(store_number="TestStore")
    assert create_store(mock_row()).__repr__() == test_store.__repr__()

def test_create_order():
    test_order = Order(customer='TestCustomer',
                       po_number='TestPO',
                       dept_number='TestDept',
                       start_date=datetime(2016, 10, 31),
                       cancel_date=datetime(2016, 11, 11),
                       create_date=datetime(2016, 10, 13))
    assert create_order(mock_row(), mock_settings()).__repr__() == test_order.__repr__()

def test_is_header_row():
    assert is_header_row(mock_row()) == False

def test_new_order():
    test_item = Item(upc="TestUpc",
                     style="TestStyle",
                     cost=500.0,
                     retail=1200.0,
                     qty=5)
    test_store = Store(store_number="TestStore")
    test_order = Order(customer='TestCustomer',
                       po_number='TestPO',
                       dept_number='TestDept',
                       start_date=datetime(2016, 10, 31),
                       cancel_date=datetime(2016, 11, 11),
                       create_date=datetime(2016, 10, 13))
    test_store.items.append(test_item)
    test_order.stores.append(test_store)
    order = new_order(mock_row(), mock_settings(), create_item(mock_row()))
    assert stringify_order(order) == stringify_order(test_order)