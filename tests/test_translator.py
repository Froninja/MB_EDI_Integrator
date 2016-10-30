import csv
import sys
from datetime import datetime
from src.models.models import Invoice, Item
from src.translate.translator import (generate_sscc, get_store_info, check_upc_exceptions,
                                      assign_items, get_invoice_info, get_shipping_info)

def mock_destination_log():
    with open('td_log.txt', 'w') as log:
        writer = csv.writer(log)
        writer.writerow(['TestCust', 'TestDest', '0001', '0123', 'TestName'])
        writer.writerow(['Saks Fifth Avenue', 'Direct - #689', '0689', '0385', ''])
        writer.writerow(["Bloomingdale's", 'BLM - CHESTNUT HILL - STORE# 11', '0011', 'SF', 'CHESTNUT HILL'])

def mock_upc_log():
    with open('tu_log.txt', 'w') as log:
        writer = csv.writer(log)
        writer.writerow(['TestCust', 'TestStyle', 'TestUpc12345'])

def mock_settings():
    settings = {
        'File Paths': {
            'Destination Log': 'td_log.txt',
            'UPC Exception Log': 'tu_log.txt',
            'Shipping Log': r'L:\Shipping\BUSA SHIPMENTS\UPS_EACH_SHIPMENT_EXPORT.csv'
            },
        'SQL Settings': {
            'Invoice Query': 'SELECT DocNum, Date, Style, Stone, Color, Finish, Length, Pieces, Cost, Destination, RingUpc, Upc FROM EDI_Invoice_Info WHERE Date >= %s AND DocNum IN ({})',
            'Connection String': 'DRIVER={SQL Server};SERVER=10.0.1.93;DATABASE=LFL;UID=amm;PWD=amm'
            }
        }
    return settings

def mock_query_rows():
    return [{'DocNum': '12345', 'Style': 'TestStyle', 'Stone': 'TS', 'Color': 'Y', 'Finish': 'F',
             'Length': 7, 'Upc': 'TestUpc12345', 'RingUpc': None, 'Destination': 'TestDest',
             'Pieces': 2, 'Cost': 100.0}]

def mock_invoices():
    return {'12345': Invoice(invoice_number='12345', customer='TestCust')}

def test_generate_sscc_with_12345():
    assert generate_sscc('12345') == '803276200000123459'

def test_generate_sscc_with_none():
    assert generate_sscc(None) == '803276200000000000'

def test_generate_sscc_with_bob():
    assert generate_sscc('bob') == '803276200000000000'

def test_get_store_info_with_valid_destination():
    mock_destination_log()
    inv = Invoice()
    inv.customer = 'TestCust'
    inv = get_store_info(inv, 'TestDest', mock_settings())
    assert inv.store_number == '0001'
    assert inv.dc_number == '0123'
    assert inv.store_name == 'TestName'

def test_check_upc_exceptions_with_present_value():
    mock_upc_log()
    item = Item(style='TestStyle')
    item.upc = check_upc_exceptions(item, 'TestCust',
                                    mock_settings()['File Paths']['UPC Exception Log'])
    assert item.upc == 'TestUpc12345'

def test_check_upc_exceptions_with_missing_style():
    mock_upc_log()
    item = Item(style='BadStyle')
    item.upc = check_upc_exceptions(item, 'TestCust',
                                    mock_settings()['File Paths']['UPC Exception Log'])
    assert item.upc == None

def test_check_upc_exceptions_with_missing_customer():
    mock_upc_log()
    item = Item(style='TestStyle')
    item.upc = check_upc_exceptions(item, 'BadCust',
                                    mock_settings()['File Paths']['UPC Exception Log'])
    assert item.upc == None

def test_assign_items_with_well_formed_data():
    invoices = mock_invoices()
    final_invoices = mock_invoices()
    final_invoices['12345'].items.append(Item(style='TestStyle-TS-Y-F-7',
                                              qty=2,
                                              cost=50.0,
                                              upc='TestUpc12345'))
    rows = mock_query_rows()
    invoices = assign_items(rows, invoices, mock_settings())
    item_a = invoices['12345'].items[0]
    item_b = final_invoices['12345'].items[0]
    assert item_a.style == item_b.style
    assert item_a.upc == item_b.upc
    assert item_a.cost == item_b.cost
    assert item_a.qty == item_b.qty

class TestGetInvoiceInfo(object):
    def setup(self):
        mock_destination_log()
        mock_upc_log()
        self.test_inv = Invoice(invoice_number='59128',
                                customer='Saks Fifth Avenue',
                                store_number='0689',
                                store_name='',
                                dc_number='0385',
                                discount_code='05',
                                discount=0,
                                total_cost=4575.0,
                                total_qty=7)
        self.test_inv_mult = Invoice(invoice_number='65502',
                                     customer="Bloomingdale's",
                                     store_number='0011',
                                     store_name='CHESTNUT HILL',
                                     dc_number='SF',
                                     discount_code='05',
                                     discount=0,
                                     total_cost=1570.0,
                                     total_qty=2)
        item = Item(upc='8032762282181',
                    style='OB1403-MPB-Y-02-0.0',
                    cost=785.0,
                    qty=2)
        self.test_inv_mult.items.append(item)

    def test_get_invoice_info(self):
        invoice_list = get_invoice_info([Invoice(invoice_number='59128',
                                                 customer='Saks Fifth Avenue')],
                                        'Saks Fifth Avenue',
                                        mock_settings())
        inv = invoice_list[0]
        assert inv.__repr__() == self.test_inv.__repr__()
        
    def test_multiple_items(self):
        invoice_list = get_invoice_info([Invoice(invoice_number='65502',
                                                 customer="Bloomingdale's")],
                                        "Bloomingdale's",
                                        mock_settings())
        inv = invoice_list[0]
        for index, item in enumerate(self.test_inv_mult.items):
            assert item.__repr__() == inv.items[index].__repr__()
        assert inv.__repr__() == self.test_inv_mult.__repr__()

class TestGetShippingInfo(object):
    def setup(self):
        self.test_invoice = Invoice(invoice_number='59128',
                                    customer='Saks Fifth Avenue',
                                    sscc_number='803276200000591289',
                                    tracking_number='1ZW885Y21349335867',
                                    ship_date=datetime(2015, 12, 15),
                                    address_1='ONE WALDENBOOKS DRIVE',
                                    address_2='DC# 185 STORE# 689',
                                    city_state_zip='LA VERGNE, TN 37086')

    def test_get_shipping_info(self):
        invoice_list = get_shipping_info([Invoice(invoice_number='59128',
                                                  customer='Saks Fifth Avenue')],
                                         mock_settings())
        assert invoice_list[0].__repr__() == self.test_invoice.__repr__()