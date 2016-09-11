from src.models import invoice

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
