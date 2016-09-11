from translate.translator import OutputTranslator
from models.invoice import Invoice, Product
from datetime import datetime

"""Test values:
First Invoice: #59128
Saks Fifth Avenue
Store#: 0689
Tracking#: 1ZW885T21349335867
Ship Date: 12/15/2015
Discount Code: 05
Discount Percent: 0
SSCC: 803276200000591289
PO#: 6163130
Dept#: 0162
Distribution Center: 0185
Item Count: 7
Total Cost: $4575
Total Qty: 7
Store Name: -n/a-
Address 1: One Waldenbooks Drive
Address 2: DC# 185 Store# 689
City: LA VERGNE
State: TN
Zip: 37086
Items: CB1779 Y, OB1234 Y, OB1343 Y, OB1349 Y, OB938 Y, OB957 TP01 Y, OG326 B YW
Create Date:
"""

class TranslatorUnitTest(object):
    def __init__(self, settings):
        self.test_invoices = []
        self.test_invoice()
        self.o = OutputTranslator('Saks Fifth Avenue', settings, False, True)
        self.array = [['59128', '6163130', 0, False]]

    def run(self):
        self.o.run([['59128', '6163130', 0, False]])

    def test_invoice(self):
        inv = Invoice('59128')
        inv.customer = 'Saks Fifth Avenue'
        inv.store_number = '0689'
        inv.tracking_number = '1ZW885Y21349335867'
        inv.ship_date = datetime(2015, 12, 15)
        inv.discount_code = '05'
        inv.discount_percent = 0
        inv.sscc = '803276200000591289'
        inv.purchase_order_number = '6163130'
        inv.department_number = '0162'
        inv.distribution_center = '0185'
        inv.item_count = 7
        inv.total_cost = 4575
        inv.total_qty = 7
        inv.address1 = 'ONE WALDENBOOKS DRIVE'
        inv.address2 = 'DC# 185 STORE# 689'
        inv.city = 'LA VERGNE'
        inv.state = 'TN'
        inv.zip_code = '37086'
        p1 = Product('CB1779- -Y-02-42.0')
        p1.upc = '8032762238027'
        p1.qty_each = 1
        p1.unit_cost = 795
        inv.items.append(p1)
        p2 = Product('OB1234- -Y-02-0')

        self.test_invoices.append(inv)

    def test(self):
        test_inv = self.test_invoices[0]
        inv = self.o.invoice_list[0]
        if inv.invoice_number == test_inv.invoice_number:
            print("Invoice Number PASS")
        else:
            print("\n===Invoice Number FAIL===\n===Was %s; Should be %s===\n" % (inv.invoice_number, test_inv.invoice_number))
        if inv.customer == test_inv.customer:
            print("Customer Name PASS")
        else:
            print("\n===Customer Name FAIL===\n===Was %s; Should be %s===\n" % (inv.customer, test_inv.customer))
        if inv.store_number == test_inv.store_number:
            print("Store Number PASS")
        else:
            print("\n===Store Number FAIL===\n===Was %s; Should be %s===\n" % (inv.store_number, test_inv.store_number))
        if inv.tracking_number == test_inv.tracking_number:
            print("Tracking Number PASS")
        else:
            print("\n===Tracking Number FAIL===\n===Was %s; Should be %s===\n" % (inv.tracking_number, test_inv.tracking_number))
        if inv.ship_date == test_inv.ship_date:
            print("Ship Date PASS")
        else:
            print("\n===Ship Date FAIL===\n===Was %s; Should be %s===\n" % (inv.ship_date.strftime("%m/%d/%Y"), test_inv.ship_date.strftime("%m/%d/%Y")))
        if inv.discount_code == test_inv.discount_code:
            print("Discount Code PASS")
        else:
            print("\n===Discount Code FAIL===\n===Was %s; Should be %s===\n" % (inv.discount_code, test_inv.discount_code))
        if inv.discount_percent == test_inv.discount_percent:
            print("Discount Percent PASS")
        else:
            print("\n===Discount Percent FAIL===\n===Was %s; Should be %s===\n" % (inv.discount_percent, test_inv.discount_percent))
        if inv.sscc == test_inv.sscc:
            print("SSCC PASS")
        else:
            print("\n===SSCC FAIL===\n===Was %s; Should be %s===\n" % (inv.sscc, test_inv.sscc))
        if inv.purchase_order_number == test_inv.purchase_order_number:
            print("PO Number PASS")
        else:
            print("\n===PO Number FAIL===\n===Was %s; Should be %s===\n" % (inv.purchase_order_number, test_inv.purchase_order_number))
        if inv.department_number == test_inv.department_number:
            print("Dept Number PASS")
        else:
            print("\n===Dept Number FAIL===\n===Was %s; Should be %s===\n" % (inv.department_number, test_inv.department_number))
        if inv.distribution_center == test_inv.distribution_center:
            print("DC Number PASS")
        else:
            print("\n===DC Number FAIL===\n===Was %s; Should be %s===\n" % (inv.distribution_center, test_inv.distribution_center))
        if inv.item_count == test_inv.item_count:
            print("Item Count PASS")
        else:
            print("\n===Item Count FAIL===\n===Was %s; Should be %s===\n" % (inv.item_count, test_inv.item_count))
        if inv.total_cost == test_inv.total_cost:
            print("Total Cost PASS")
        else:
            print("\n===Total Cost FAIL===\n===Was %s; Should be %s===\n" % (inv.total_cost, test_inv.total_cost))
        if inv.total_qty == test_inv.total_qty:
            print("Total Qty PASS")
        else:
            print("\n===Total Qty FAIL===\n===Was %s; Should be %s===\n" % (inv.total_qty, test_inv.total_qty))
