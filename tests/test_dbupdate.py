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
                     qty=5,
                     shipped_cost=None)
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

def test_check_for_store_with_no_store():
    test_order = create_order(mock_row(), mock_settings())
    assert check_for_store(mock_row(), test_order) == False

def test_check_for_store_with_store():
    test_store = create_store(mock_row())
    test_order = create_order(mock_row(), mock_settings())
    test_order.stores.append(test_store)
    store = check_for_store(mock_row(), test_order)
    assert store.__repr__() == test_store.__repr__()

def test_check_for_order_with_order():
    orders = { mock_row()[1]: create_order(mock_row(), mock_settings()) }
    assert stringify_order(check_for_order(mock_row(), orders)) == stringify_order(list(orders.values())[0])

def test_check_for_order_with_no_order():
    orders = dict()
    assert check_for_order(mock_row(), orders) == False

def test_compare_orders_same():
    order1 = create_order(mock_row(), mock_settings())
    order2 = create_order(mock_row(), mock_settings())
    assert compare_orders(order1, order2) == True

def test_compare_orders_meaningfully_different():
    order1 = create_order(mock_row(), mock_settings())
    order2 = create_order(mock_row(), mock_settings())
    order2.total_cost = 700.0
    assert compare_orders(order1, order2) == False

def test_compare_orders_meaningless_difference():
    order1 = create_order(mock_row(), mock_settings())
    order2 = create_order(mock_row(), mock_settings())
    order2.shipped_cost = 500.0
    assert compare_orders(order1, order2) == True

def test_collect_orders():
    reader = ExportReader()
    reader.collect_orders()
    test_orders = {
        '1702169': Order(po_number='1702169',
                         customer="Bloomingdale's",
                         dept_number='0707',
                         total_cost=1010.0,
                         total_retail=2220.0,
                         total_qty=1,
                         create_date=datetime(2016, 10, 6),
                         start_date=datetime(2016, 10, 6),
                         cancel_date=datetime(2016, 12, 12),
                         stores=[
                             Store(store_number='0062',
                                   total_cost=1010.0,
                                   total_retail=2220.0,
                                   total_qty=1,
                                   items=[
                                       Item(upc='8032762269069',
                                            style='12',
                                            cost=1010.0,
                                            retail=2220.0,
                                            qty=1)
                                       ])
                             ]),
        '5902463': Order(po_number='5902463',
                         customer="Bloomingdale's",
                         dept_number='0707',
                         total_cost=230.0,
                         total_retail=505.0,
                         total_qty=1,
                         create_date=datetime(2016, 10, 13),
                         start_date=datetime(2016, 9, 27),
                         cancel_date=datetime(2016, 11, 18),
                         stores=[
                             Store(store_number='0062',
                                   total_cost=230.0,
                                   total_retail=505.0,
                                   total_qty=1,
                                   items=[
                                       Item(upc='8032762183952',
                                            style='12',
                                            cost=230.0,
                                            retail=505.0,
                                            qty=1)
                                       ])
                             ]),
        '2942386': Order(po_number='2942386',
                         customer="Bloomingdale's",
                         dept_number='0707',
                         total_cost=14350.0,
                         total_retail=31555.0,
                         total_qty=21,
                         create_date=datetime(2016, 10, 13),
                         start_date=datetime(2016, 10, 31),
                         cancel_date=datetime(2016, 11, 11),
                         stores=[
                             Store(store_number='0022',
                                   total_cost=2575.0,
                                   total_retail=5665.0,
                                   total_qty=3,
                                   items=[
                                       Item(upc='8032762173441',
                                            style='12',
                                            cost=1740.0,
                                            retail=3830.0,
                                            qty=1),
                                       Item(upc='8032762123033',
                                            style='12',
                                            cost=450.0,
                                            retail=990.0,
                                            qty=1),
                                       Item(upc='8032762276371',
                                            style='12',
                                            cost=385.0,
                                            retail=845.0,
                                            qty=1)
                                       ]),
                             Store(store_number='0060',
                                   total_cost=495.0,
                                   total_retail=1090.0,
                                   total_qty=1,
                                   items=[
                                       Item(upc='8032762276159',
                                            style='12',
                                            cost=495.0,
                                            retail=1090.0,
                                            qty=1)
                                       ]),
                             Store(store_number='0006',
                                   total_cost=835.0,
                                   total_retail=1835.0,
                                   total_qty=2,
                                   items=[
                                       Item(upc='8032762123033',
                                            style='12',
                                            cost=450.0,
                                            retail=990.0,
                                            qty=1),
                                       Item(upc='8032762276371',
                                            style='12',
                                            cost=385.0,
                                            retail=845.0,
                                            qty=1)
                                       ]),
                             Store(store_number='0002',
                                   total_cost=2280.0,
                                   total_retail=5015.0,
                                   total_qty=3,
                                   items=[
                                       Item(upc='8032762265313',
                                            style='12',
                                            cost=1115.0,
                                            retail=2450.0,
                                            qty=1),
                                       Item(upc='8032762169000',
                                            style='12',
                                            cost=780.0,
                                            retail=1720.0,
                                            qty=1),
                                       Item(upc='8032762276371',
                                            style='12',
                                            cost=385.0,
                                            retail=845.0,
                                            qty=1)
                                       ]),
                             Store(store_number='0016',
                                   total_cost=2320.0,
                                   total_retail=5095.0,
                                   total_qty=3,
                                   items=[
                                       Item(upc='8032762174141',
                                            style='12',
                                            cost=820.0,
                                            retail=1800.0,
                                            qty=1),
                                       Item(upc='8032762265313',
                                            style='12',
                                            cost=1115.0,
                                            retail=2450.0,
                                            qty=1),
                                       Item(upc='8032762276371',
                                            style='12',
                                            cost=385.0,
                                            retail=845.0,
                                            qty=1)
                                       ]),
                             Store(store_number='0010',
                                   total_cost=450.0,
                                   total_retail=990.0,
                                   total_qty=1,
                                   items=[
                                       Item(upc='8032762123033',
                                            style='12',
                                            cost=450.0,
                                            retail=990.0,
                                            qty=1)
                                       ]),
                             Store(store_number='0003',
                                   total_cost=1115.0,
                                   total_retail=2450.0,
                                   total_qty=1,
                                   items=[
                                       Item(upc='8032762265313',
                                            style='12',
                                            cost=1115.0,
                                            retail=2450.0,
                                            qty=1)
                                       ]),
                             Store(store_number='0011',
                                   total_cost=1230.0,
                                   total_retail=2710.0,
                                   total_qty=2,
                                   items=[
                                       Item(upc='8032762169000',
                                            style='12',
                                            cost=780.0,
                                            retail=1720.0,
                                            qty=1),
                                       Item(upc='8032762123033',
                                            style='12',
                                            cost=450.0,
                                            retail=990.0,
                                            qty=1)
                                       ]),
                             Store(store_number='0034',
                                   total_cost=780.0,
                                   total_retail=1720.0,
                                   total_qty=1,
                                   items=[
                                       Item(upc='8032762169000',
                                            style='12',
                                            cost=780.0,
                                            retail=1720.0,
                                            qty=1)
                                       ]),
                             Store(store_number='0008',
                                   total_cost=385.0,
                                   total_retail=845.0,
                                   total_qty=1,
                                   items=[
                                       Item(upc='8032762276371',
                                            style='12',
                                            cost=385.0,
                                            retail=845.0,
                                            qty=1)
                                       ]),
                             Store(store_number='0030',
                                   total_cost=1115.0,
                                   total_retail=2450.0,
                                   total_qty=1,
                                   items=[
                                       Item(upc='8032762265313',
                                            style='12',
                                            cost=1115.0,
                                            retail=2450.0,
                                            qty=1)
                                       ]),
                             Store(store_number='0014',
                                   total_cost=385.0,
                                   total_retail=845.0,
                                   total_qty=1,
                                   items=[
                                       Item(upc='8032762276371',
                                            style='12',
                                            cost=385.0,
                                            retail=845.0,
                                            qty=1)
                                       ]),
                             Store(store_number='0017',
                                   total_cost=385.0,
                                   total_retail=845.0,
                                   total_qty=1,
                                   items=[
                                       Item(upc='8032762276371',
                                            style='12',
                                            cost=385.0,
                                            retail=845.0,
                                            qty=1)
                                       ])
                             ])
        }
    for order in test_orders.values():
        assert compare_orders(order, reader.orders[order.po_number]) is True