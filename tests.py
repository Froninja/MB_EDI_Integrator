from src.models import invoice
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

#region invoice

def test_generate_sscc_with_12345():
    assert invoice.generate_sscc('12345') == '803276200000123459'

def test_discount_with_string_non_zero():
    inv = invoice.Invoice('12345')
    inv.discount('5')
    assert inv.discount_percent == 5 and inv.discount_code == "08"

def test_discount_with_int_non_zero():
    inv = invoice.Invoice('12345')
    inv.discount(5)
    assert inv.discount_percent == 5 and inv.discount_code == "08"

def test_discount_with_string_zero():
    inv = invoice.Invoice('12345')
    inv.discount('0')
    assert inv.discount_percent == 0 and inv.discount_code == "05"

def test_discount_with_int_zero():
    inv = invoice.Invoice('12345')
    inv.discount(0)
    assert inv.discount_percent == 0 and inv.discount_code == "05"

def test_discount_with_none():
    inv = invoice.Invoice('12345')
    inv.discount(None)
    assert inv.discount_percent == 0 and inv.discount_code == "05"

def test_get_dept_num_with_true():
    inv = invoice.Invoice('12345')
    inv.get_dept_num(True, '100', '200')
    assert inv.department_number == '0200'

def test_get_dept_num_with_zero():
    inv = invoice.Invoice('12345')
    inv.get_dept_num(0, '100', '200')
    assert inv.department_number == '0100'

#endregion
