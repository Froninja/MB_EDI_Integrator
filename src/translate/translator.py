from os import path
from datetime import datetime, date, timedelta
from PyQt5 import QtWidgets, QtCore
import pymssql
import csv
from src.models.models import Invoice, Item
from src.db.db import get_session, get_sql_connection
from src.ui.warnings import (OverWriteDialog, UPCWarningDialog,
                             TrackingWarningDialog, StoreWarningDialog, DescriptionWarningDialog,)
from src.translate.validater import DbValidater


class OutputTranslator(QtCore.QObject):
    """Single instance class to add requisite information and output for a list
of invoices
    """
    def __init__(self, customer, settings, append=False, test=False):
        QtCore.QObject.__init__(self)
        self.progress = 0
        self.database = get_session(settings['File Paths']['PO Database File'])
        self.customer = customer
        self.settings = settings
        self.invoice_list = []
        self.append = append
        self.test = test
        self.get_customer_settings()
        self.validater = None

    def get_validater(self):
        self.validater = DbValidater(self.invoice_list, self.database)

    def run(self, inv_array):
        self.generate_invoices(inv_array)
        self.invoice_list = get_shipping_info(self.invoice_list, self.settings)
        if self.invoice_list:
            self.invoice_list = get_invoice_info(self.invoice_list, self.customer, self.settings)
            if self.invoice_list:
                self.get_validater()
                if not self.validater.check_po():
                    print("%s Operation canceled by user" % datetime.now())
                    return False
                return True
        return False

    def get_customer_settings(self):
        self.customer_settings = self.settings['Customer Settings'][self.customer]

    def generate_invoices(self, inv_array):
        print("%s Starting invoice generation" % datetime.now())
        for row in inv_array:
            if len(row[0]) > 0:
                invoice = Invoice(invoice_number=row[0],
                                  customer=self.customer,
                                  po_number=row[1])
                invoice.discount(row[2])
                invoice.dept_number(row[3], self.customer_settings['Asset Department'],
                                    self.customer_settings['Memo Department'])
                self.invoice_list.append(invoice)
                print("%s Created Invoice# %s, with PO# %s, Dept# %s, and discount %s"
                      % (datetime.now(), invoice.invoice_number, invoice.po_number,
                         invoice.dept_number, invoice.discount))

        print("%s Ending generation. Generated %s invoices"
              % (datetime.now(), len(self.invoice_list)))
        self.progress += 1

    def check_for_existing_file(self):
        return (path.isfile(self.settings['File Paths']['MAPDATA Path'] + '\\'
                            + self.customer_settings['ASN File'])
                or path.isfile(self.settings['File Paths']['MAPDATA Path'] + '\\'
                               + self.customer_settings['Invoice File']))

    def write_output(self):
        print("%s Beginning Output" % datetime.now())
        header_temp, inv_temp, item_temp = get_output_templates()
        if self.check_for_existing_file():
            m = OverWriteDialog()
            if m.exec_() == QtWidgets.QMessageBox.Yes:
                self.append = True
        if self.append is False:
            output_string = output_header_string(header_temp, self.customer_settings)
            mode = 'w'
        else:
            output_string = ''
            mode = 'a'
        for invoice in self.invoice_list:
            add_output_row(self.database, invoice)
            output_string += output_inv_string(inv_temp, invoice)
            for item in invoice.items:
                output_string += output_item_string(item_temp, item)
        with open(self.settings['File Paths']['MAPDATA Path'] + '\\'
                  + self.customer_settings['ASN File'], mode) as file:
            file.write(output_string)
        with open(self.settings['File Paths']['MAPDATA Path'] + '\\'
                  + self.customer_settings['Invoice File'], mode) as file:
            file.write(output_string)
        self.database.commit()
        print("%s Output successful" % datetime.now())
        self.progress += 1


def assign_shipping_info(invoice: Invoice, ship_log: str):
    invoice = check_ship_log(invoice, ship_log)
    if invoice.tracking_number is None:
        dialog = TrackingWarningDialog(invoice.invoice_number)
        dialog.exec_()
        if dialog.confirmed is True:
            invoice.tracking_number = dialog.tracking
        else:
            return False
    return invoice

def check_ship_log(invoice, ship_log):
    for line in reversed(open(ship_log, 'r').readlines()):
        line = line.replace('"', '').split(',')
        inv_cell = line[10].split(' ')
        for seg in inv_cell:
            if len(seg) == 5 and seg == str(invoice.invoice_number):
                invoice.tracking_number = line[9]
                invoice.ship_date = datetime.strptime(line[0], '%Y%m%d')
                invoice.address_1 = line[2]
                invoice.address_2 = line[3]
                invoice.city_state_zip = line[4] + ', ' + line[5] + ' ' + line[6][:5]
    return invoice

def generate_sscc(inv_num):
    """Generates a GS1 18 digit SSCC number from the supplied invoice number"""
    try:
        sscc_string = str(80327620000000000 + int(inv_num))
        check_sum = 0
        for index, digit in enumerate(sscc_string):
            if index % 2 == 0:
                check_sum += int(digit) * 3
            else:
                check_sum += int(digit)
        check_digit = ((check_sum + 9) // 10 * 10) - check_sum
        return sscc_string + str(check_digit)
    except (TypeError, ValueError):
        return '803276200000000000'

def get_shipping_info(invoice_list: list, settings: dict):
    """Returns a new sorted invoice list populated with data from the shipping log"""
    for invoice in invoice_list:
        invoice = assign_shipping_info(invoice, settings['File Paths']['Shipping Log'])
        invoice.sscc_number = generate_sscc(invoice.invoice_number)
        if not invoice:
            return False
    return invoice_list

def get_invoice_info(invoice_list: list, customer: str, settings: dict):
    """Returns a new sorted invoice list populated with data from the server"""
    invoices = {inv.invoice_number: inv for inv in invoice_list}
    params = get_params(600, invoice_list)
    sql = settings['SQL Settings']['Invoice Query'].format(','.join(['%s'] * (len(params) - 1)))
    with (get_sql_connection(settings['SQL Settings']['Connection String']).
          cursor(as_dict=True)) as cursor:
        cursor.execute(sql,params)
        testsql = (sql % params)
        query_rows = cursor.fetchall()
        invoices = assign_items(query_rows, invoices, settings)
        invoices = assign_stores(query_rows, invoices, settings)
        [inv.get_totals() for inv in invoices.values()]
    return sort_invoices([inv for inv in invoices.values()])

def assign_items(rows: list, invoices: dict, settings: dict):
    for row in rows:
        invoice = invoices[str(row['DocNum'])]
        item = Item(style='-'.join([row['Style'], row['Stone'], row['Color'],
                                    row['Finish'], str(row['Length'])]),
                    qty=row['Pieces'],
                    cost=row['Cost'] / row['Pieces'],
                    upc=(row['Upc'] or row['RingUpc']))
        item.upc = check_upc_exceptions(item, invoice.customer,
                                        settings['File Paths']['UPC Exception Log'])
        if item.upc is None:
            item.upc = upc_not_found(item.style, invoice.invoice_number,
                                     settings, invoice.customer)
            if not item.upc:
                return False
        if item.upc in [it.upc for it in invoice.items]:
            orig_item = next((it for it in invoice.items if it.upc == item.upc))
            orig_item.qty += item.qty
        else:
            invoice.items.append(item)
    return invoices

def assign_stores(rows: list, invoices: dict, settings: dict):
    for row in rows:
        invoice = invoices[str(row['DocNum'])]
        if invoice.store_number is None:
            invoice = get_store_info(invoice, row['Destination'], settings)
            if not invoice.store_number:
                return False
    return invoices

def get_store_info(invoice: Invoice, destination: str, settings: dict):
    """Checks the destination file for store info and assigns to the invoice. If the destination
    is not found, requests user input. Returns False if the user cancels operation"""
    with open(settings['File Paths']['Destination Log'], 'r') as dest_log:
        dest_reader = csv.reader(dest_log)
        for row in dest_reader:
            if len(row) > 0 and row[0] == invoice.customer and row[1] == destination:
                invoice.store_number = row[2].zfill(4)
                invoice.dc_number = row[3].zfill(4)
                invoice.store_name = row[4]
    if invoice.store_number is None:
        invoice = store_not_found(invoice, destination, settings)
    return invoice

def store_not_found(invoice: Invoice, destination: str, settings: dict):
    """Opens a warning dialog and assigns user entered store info to invoice and persistant file.
    Returns False if user cancels operation"""
    dialog = StoreWarningDialog(destination, invoice.invoice_number)
    dialog.exec_()
    if dialog.confirmed == True:
        inv = invoice
        inv.store_number = dialog.store_num
        inv.dc_number = dialog.dc_num
        inv.store_name = dialog.store_name
        write_new_destination(dialog, destination, settings, inv.customer)
        return inv
    return False

def write_new_destination(dialog: StoreWarningDialog, destination: str, settings: dict,
                          customer: str):
    """Writes the new user-entered information to the log"""
    with open(settings['File Paths']['Destination Log'], 'a') as dest_log:
        dest_writer = csv.writer(dest_log)
        dest_writer.writerow([customer, destination,
                              dialog.store_num, dialog.dc_num, dialog.store_name])

def upc_not_found(style: str, inv_num: str, settings: dict, customer: str):
    dialog = UPCWarningDialog(style, inv_num)
    dialog.exec_()
    if dialog.confirmed == True:
        write_new_upc(dialog.upc, style, settings, customer)
        return str(dialog.upc).strip()
    return False

def write_new_upc(upc: str, style: str, settings: dict, customer: str):
    """Writes a new user entered UPC to the log"""
    with open(settings['File Paths']['UPC Exception Log'], 'a') as upc_log:
        upc_writer = csv.writer(upc_log)
        upc_writer.writerow([customer, style, str(upc).strip()])

def get_params(age: int, invoice_list: list):
    """Returns a tuple of parameters to use in a SQL query. Tuple format is:
    (minimum date, invoice #1, ... invoice #n)"""
    min_date = datetime.now() - timedelta(age)
    return tuple([min_date] + [inv.invoice_number for inv in invoice_list])

def check_upc_exceptions(item, customer, exception_log):
    with open(exception_log, 'r') as exception_list:
        except_reader = csv.reader(exception_list)
        for row in except_reader:
            if row[:2] == [customer, item.style]:
                return row[2]
    return item.upc

def sort_invoices(invoice_list: list):
    """Returns the invoice list sorted by PO Number and store number"""
    invoice_list = sorted(invoice_list, key=lambda inv: inv.store_number)
    invoice_list = sorted(invoice_list, key=lambda inv: inv.po_number)
    return invoice_list

def get_output_templates():
    """Returns templates for formatting header, invoice, item output"""
    with open("OutputTemplates/HeaderTemplate.txt", 'r') as header_file:
        header = header_file.readline() + '\n'
    with open("OutputTemplates/InvoiceTemplate.txt", 'r') as inv_file:
        inv = inv_file.readline() + '\n'
    with open("OutputTemplates/ItemTemplate.txt", 'r') as item_file:
        item = item_file.readline() + '\n'
    return header, inv, item

def output_header_string(template, customer_settings):
    output = template.replace('ReceiverInvID', customer_settings['Invoice ID'])
    output = output.replace('ReceiverShipID', customer_settings['ASN ID'])
    output = output.replace('VersionNum', ('00' + customer_settings['EDI Version'])[:5])
    return output

def output_inv_string(template, invoice):
    output = template.replace('Inv', invoice.invoice_number)
    output = output.replace('Store', invoice.store_number)
    output = output.replace('Track', invoice.tracking_number)
    try:
        output = output.replace('ShipDate', invoice.ship_date.strftime('%Y%m%d'))
    except AttributeError:
        output = output.replace('ShipDate', datetime.now().strftime('%Y%m%d'))
    output = output.replace('DiscCode', invoice.discount_code)
    output = output.replace('Disc', str(invoice.discount))
    output = output.replace('SSCC', invoice.sscc_number)
    output = output.replace('PO', invoice.po_number)
    output = output.replace('Dept', invoice.dept_number)
    output = output.replace('DC', invoice.dc_number)
    output = output.replace('Qty', str(invoice.total_qty))
    try:
        output = output.replace('CreateDate', invoice.create_date.strftime("%Y/%m/%d"))
    except AttributeError:
        output = output.replace('CreateDate', datetime.now().strftime("%Y/%m/%d"))
    return output

def output_item_string(template, item):
    """Returns a formatted string from the supplied template and invoice"""
    output = template.replace('Style', item.style)
    output = output.replace('UPC', item.upc)
    output = output.replace('Qty', str(int(item.qty)))
    output = output.replace('Cost', str(item.cost))
    return output

def add_output_row(session, invoice):
    """Creates an OutputRecord for the given invoice and adds it to the provided session"""
    """output = OutputRecord(inv_num=invoice.invoice_number,
                          po_num=invoice.purchase_order_number,
                          store_num=invoice.store_number,
                          store_name=invoice.store_name,
                          dc_num=invoice.distribution_center,
                          dept_num=invoice.department_number,
                          total_qty=int(invoice.total_qty),
                          ship_date=datetime.now(),
                          sscc=invoice.sscc,
                          tracking=invoice.tracking_number,
                          address1=invoice.address1,
                          address2=invoice.address2,
                          city_state_zip=(invoice.city + ', ' + invoice.state
                                          + ' ' + invoice.zip_code))"""
    session.add(invoice)


