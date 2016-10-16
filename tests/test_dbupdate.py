from src.db.dbupdate import *
from src.models.models import Order, Store, Item

def mock_row():
    return [
        "TestClient",
        "TestPO",
        "TestDateS",
        "TestDateC",
        "TestStore",
        "TestUpc",
        "TestStyle",
        500.0,
        1200.0,
        5,
        "TestDateCr",
        "TestDept"
    ]

def test_create_item():
    test_item = Item(upc="TestUpc",
                     style="TestStyle",
                     cost=500.0,
                     qty=5)
    assert create_item(mock_row()).__repr__() == test_item.__repr__()

def test_create_store():
    test_store = Store(store_number="TestStore")
    assert create_store(mock_row()).__repr__() == test_store.__repr__()

def test_is_header_row():
    assert is_header_row(mock_row()) == False