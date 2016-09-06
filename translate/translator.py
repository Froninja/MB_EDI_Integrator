from datetime import datetime, date, timedelta
import os.path
from models.invoice import Invoice, Product
from db.podb import PurchaseOrderDB
from ui.warnings import (OverWriteDialog, UPCWarningDialog,
                         TrackingWarningDialog, StoreWarningDialog, DescriptionWarningDialog,)
from translate.validater import DbValidater
from PyQt5 import QtWidgets, QtCore
import pymssql


class OutputTranslator(QtCore.QObject):
    """Single instance class to add requisite information and output for a list
of invoices
    """
    def __init__(self, customer, settings, append=False, test=False):
        QtCore.QObject.__init__(self)
        self.progress = 0
        self.customer = customer
        self.settings = settings
        self.invoice_list = []
        self.append = append
        self.test = test
        self.get_customer_settings()
        self.validater = None

    def initiate_db(self):
        self.po_db = PurchaseOrderDB(self.settings['File Paths']['PO Database File'])

    def run(self, inv_array):
        self.generate_invoices(inv_array)
        if not self.get_ship_data():
            return False
        if not self.assign_destinations():
            return False
        self.assign_items()
        if not self.assign_upcs():
            return False
        self.validater = DbValidater(self.settings['File Paths']['PO Database File'],
                                     self.invoice_list)
        if not self.validater.check_po():
            print("%s Operation canceled by user" % datetime.now())
            return False
        return True

    def get_customer_settings(self):
        self.customer_settings = self.settings['Customer Settings'][self.customer]

    def generate_invoices(self, inv_array):
        print("%s Starting invoice generation" % datetime.now())
        for row in inv_array:
            if len(row[0]) > 0:
                invoice = Invoice(row[0])
                invoice.purchase_order_number = row[1]
                invoice.discount(row[2])
                invoice.customer = self.customer
                invoice.get_dept_num(row[3], self.customer_settings['Asset Department'],
                                     self.customer_settings['Memo Department'])
                self.invoice_list.append(invoice)
                print("%s Created Invoice# %s, with PO# %s, Dept# %s, and discount %s"
                      % (datetime.now(), invoice.invoice_number, invoice.purchase_order_number,
                         invoice.department_number, invoice.discount_percent))

        self.invoice_list = sorted(sorted(self.invoice_list, key=lambda inv: inv.store_number),
                                   key=lambda inv: inv.purchase_order_number)
        print("%s Ending generation. Generated %s invoices"
              % (datetime.now(), len(self.invoice_list)))
        self.progress += 1

    def get_ship_data(self):
        print("%s Querying shipping info" % datetime.now())
        for invoice in self.invoice_list:
            invoice.shipping_information(self.settings['File Paths']['Shipping Log'])
            if invoice.tracking_number == '':
                self.w = TrackingWarningDialog(invoice.invoice_number)
                self.w.exec_()
                if self.w.confirmed is True:
                    invoice.tracking_number = self.w.tracking.strip('\n').strip('\r')
                    invoice.shipping_information_from_tracking(self.settings['File Paths']
                                                               ['Shipping Log'])
                else:
                    return False
            invoice.get_SSCC()
        print("%s Shipping info complete" % datetime.now())
        self.progress += 1
        return True

    def get_destinations(self):
        """
        Returns a dictionary of row objects indexed by invoice number based
        on the list of invoices, destionation query from settings, and current
        year
        """
        print("%s Querying destinations" % datetime.now())
        with get_sql_connection(self.settings['SQL Settings']['Connection String']) as conn:
            with conn.cursor(as_dict=True) as cursor:
                min_date = date.today() - timedelta(365)
                sql = (self.settings['SQL Settings']['Destination Query']
                       .format(','.join(['%s'] * len(self.invoice_list))))

                params = [min_date] + [inv.invoice_number for inv in self.invoice_list]
                cursor.execute(sql, tuple(params))
                query_dict = dict()
                for row in cursor:
                    query_dict[str(row['NrDocF'])] = row
                sql = (self.settings['SQL Settings']['Memo Destination Query']
                       .format(','.join(['%s'] * len(self.invoice_list))))

                params = [min_date] + [inv.invoice_number for inv in self.invoice_list]
                cursor.execute(sql, tuple(params))
                for row in cursor:
                    if str(row['NrDocF']) not in query_dict:
                        query_dict[str(row['NrDocF'])] = row
        print("%s Successfully queried %s destinations" % (datetime.now(), len(query_dict)))
        self.progress += 1
        return query_dict

    def get_items(self):
        """
        Returns a dictionary of lists of row objects indexed by invoice
        number based on the list of invoices, invoice query from settings, and
        current year
        """
        print("%s Querying items" % datetime.now())
        with get_sql_connection(self.settings['SQL Settings']['Connection String']) as conn:
            with conn.cursor(as_dict=True) as cursor:
                min_date = date.today() - timedelta(365)
                sql = (self.settings['SQL Settings']['Invoice Query']
                       .format(','.join(['%s'] * len(self.invoice_list))))
                params = [min_date] + [inv.invoice_number for inv in self.invoice_list]
                cursor.execute(sql, tuple(params))
                query_dict = dict()
                for row in cursor:
                    if str(row['numdoc']) not in query_dict:
                        query_dict[str(row['numdoc'])] = []
                    query_dict[str(row['numdoc'])].append(row)
        print("%s Successfully queried %s items" % (datetime.now(), len(query_dict)))
        self.progress += 1
        return query_dict

    def get_upcs(self):
        """
        Returns a dictionary of row objects indexed by style number based on
        items returned by get_items and UPC queries from settings
        """
        print("%s Querying UPCs" % datetime.now())
        ring_list = ''
        non_ring_list = ''
        query = self.get_items()
        for invoice in query.values():
            for row in invoice:
                if row['codmod'] not in ring_list and row['codmod'][0] == 'A':
                    ring_list += "'%s'," % row['codmod']
                elif row['codmod'] not in non_ring_list:
                    non_ring_list += "'%s'," % row['codmod']
        ring_list = ring_list.rstrip(',')
        non_ring_list = non_ring_list.rstrip(',')
        with get_sql_connection(self.settings['SQL Settings']['Connection String']) as conn:
            with conn.cursor(as_dict=True) as cursor:
                query_dict = dict()
                if len(ring_list) > 0:
                    cursor.execute(self.settings['SQL Settings']['Ring UPC Query']
                                   .format(ring_list))
                    for row in cursor:
                        query_dict['{}-{}-{}-{}-{}'.format(row['CodMod'], row['Cod'],
                                                           row['Colore'], row['Sup'],
                                                           str(row['Inch']))] = row

                if len(non_ring_list) > 0:
                    cursor.execute(self.settings['SQL Settings']['UPC Query'].format(non_ring_list))
                    for row in cursor:
                        query_dict['{}-{}-{}-{}-{}'.format(row['CodMod'], row['Cod'],
                                                           row['Colore'], row['Sup'],
                                                           str(row['Lgh']))] = row

        print("%s Successfully queried %s UPCs" % (datetime.now(), len(query_dict)))
        self.progress += 1
        return query_dict

    def assign_items(self):
        """
        Querys the SQL Server and assigns items to the appropriate invoices
        in the invoice list. If the customer requires descriptions, calls
        get_descriptions()
        """
        print("%s Assigning items to invoices" % datetime.now())
        query = self.get_items()
        for invoice in self.invoice_list:
            for row in query[invoice.invoice_number]:
                item = Product('{}-{}-{}-{}-{}'.format(row['codmod'], row['codpiet'],
                                                       row['colore'], row['codsup'],
                                                       str(row['lungh'])))

                item.qty_each = row['qtamov']
                item.unit_cost = row['valorev']/item.qty_each
                if self.customer_settings['Description Required'] == 'True':
                    item = self.get_descriptions(item, invoice)
                invoice.add_item(item)
        print("%s Items assigned" % datetime.now())
        self.progress += 1

    def get_descriptions(self, item, inv):
        """
        Searches the description file provided in settings for the provided
        style number and assigns descriptions from the file. If the style
        is not found in the file, requests descriptions from the user and
        adds them to the file
        """
        with open(self.settings['File Paths']['Description Log'], 'r') as desc_log:
            for line in desc_log:
                line = line.rstrip('\n').split(',')
                if line[0] == item.long_style:
                    item.description = line[1]
                    item.size = line[2]
                    item.color = line[3]
        if item.description == '':
            self.w = DescriptionWarningDialog(item.UPC, item.long_style, inv.invoice_number)
            self.w.exec_()
            if self.w.confirmed is True:
                item.description = self.w.description
                item.size = self.w.size
                item.color = self.w.color
                with open(self.settings['File Paths']['Description Log'], 'a') as desc_log:
                    desc_log.write("%s,%s,%s,%s\n" % (item.long_style, item.description,
                                                      item.size, item.color))
        print("%s Descriptions assigned" % datetime.now())
        return item

    def assign_destinations(self):
        """
        Queries the SQL Server for destination names, then searches the
        destination log file for a matching record and assigns store number,
        DC number and store name to each invoice
        """
        print("%s Assigning destinations to invoices" % datetime.now())
        query = self.get_destinations()
        for invoice in self.invoice_list:
            mb_dest = query[invoice.invoice_number]['DestinazioneCliente']
            with open(self.settings['File Paths']['Destination Log'], 'r') as dest_log:
                for line in dest_log:
                    line = line.split(',')
                    if line[0] == invoice.customer and line[1] == str(mb_dest):
                        invoice.store_number = line[2].zfill(4)
                        invoice.distribution_center = line[3].zfill(4)
                        invoice.store_name = line[4].rstrip('\n').rstrip('\r')
            if invoice.store_number == '':
                self.w = StoreWarningDialog(mb_dest, invoice.invoice_number)
                self.w.exec_()
                if self.w.confirmed is True:
                    invoice.store_number = self.w.store_num
                    invoice.store_name = self.w.store_name
                    invoice.distribution_center = self.w.dc_num
                    with open(self.settings['File Paths']['Destination Log'], 'a') as dest_log:
                        dest_log.write("%s,%s,%s,%s,%s\n" % (invoice.customer, mb_dest,
                                                             invoice.store_number,
                                                             invoice.distribution_center,
                                                             invoice.store_name))
                else:
                    return False
        print("%s Destinations assigned" % datetime.now())
        self.progress += 1
        return True

    def assign_upcs(self):
        print("%s Assigning UPCs to items" % datetime.now())
        query = self.get_upcs()
        for invoice in self.invoice_list:
            for item in invoice.items:
                try:
                    item.UPC = query[item.long_style]['BarCode']
                    item.UPC_exception_check(self.settings['File Paths']['UPC Exception Log'],
                                             invoice.customer)
                except KeyError:
                    item.UPC_exception_check(self.settings['File Paths']['UPC Exception Log'],
                                             invoice.customer)
                if item.UPC == '' or item.UPC is None:
                    self.w = UPCWarningDialog(item.long_style, invoice.invoice_number)
                    self.w.exec_()
                    if self.w.confirmed is True:
                        item.UPC = self.w.UPC.strip('\r').strip('\n')
                    else:
                        return False
                item.UPC_exception_check(self.settings['File Paths']['UPC Exception Log'],
                                         invoice.customer)
        print("%s UPCs assigned" % datetime.now())
        self.progress += 1
        return True

    def check_for_existing_file(self):
        return (os.path.isfile(self.settings['File Paths']['MAPDATA Path'] + '\\'
                               + self.customer_settings['ASN File'])
                or os.path.isfile(self.settings['File Paths']['MAPDATA Path'] + '\\'
                                  + self.customer_settings['Invoice File']))

    def write_output(self):
        print("%s Beginning Output" % datetime.now())
        header_temp, inv_temp, item_temp, label_temp = get_output_templates()
        if self.check_for_existing_file():
            m = OverWriteDialog()
            if m.exec_() == QtWidgets.QMessageBox.Yes:
                self.append = True
        if self.append is False:
            output_string = self.output_header_string(header_temp)
            mode = 'w'
        else:
            output_string = ''
            mode = 'a'
        label_string = ''
        for invoice in self.invoice_list:
            label_string += output_label_string(label_temp, invoice)
            output_string += self.output_inv_string(inv_temp, invoice)
            for item in invoice.items:
                output_string += output_item_string(item_temp, item)
        with open(self.settings['File Paths']['MAPDATA Path'] + '\\'
                  + self.customer_settings['ASN File'], mode) as file:
            file.write(output_string)
        with open(self.settings['File Paths']['MAPDATA Path'] + '\\'
                  + self.customer_settings['Invoice File'], mode) as file:
            file.write(output_string)
        with open(self.settings['File Paths']['Label Record File'], 'a') as file:
            file.write(label_string)
        print("%s Output successful" % datetime.now())
        self.progress += 1

    def output_header_string(self, template):
        output = template.replace('ReceiverInvID', self.customer_settings['Invoice ID'])
        output = output.replace('ReceiverShipID', self.customer_settings['ASN ID'])
        output = output.replace('VersionNum', ('00' + self.customer_settings['EDI Version'])[:5])
        return output

    def output_inv_string(self, template, invoice):
        output = template.replace('Inv', invoice.invoice_number)
        output = output.replace('Store', invoice.store_number)
        output = output.replace('Track', invoice.tracking_number)
        try:
            output = output.replace('ShipDate', invoice.ship_date.strftime('%Y%m%d'))
        except AttributeError:
            output = output.replace('ShipDate', datetime.now().strftime('%Y%m%d'))
        output = output.replace('DiscCode', invoice.discount_code)
        output = output.replace('Disc', str(invoice.discount_percent))
        output = output.replace('SSCC', invoice.SSCC)
        output = output.replace('PO', invoice.purchase_order_number)
        output = output.replace('Dept', invoice.department_number)
        output = output.replace('DC', invoice.distribution_center)
        output = output.replace('Qty', str(invoice.total_qty))
        try:
            output = output.replace('CreateDate', invoice.po_create_date.strftime("%Y/%m/%d"))
        except AttributeError:
            output = output.replace('CreateDate', datetime.now().strftime("%Y/%m/%d"))
        return output


def get_output_templates():
    """Returns templates for formatting header, invoice, item, and label output"""
    with open("OutputTemplates/HeaderTemplate.txt", 'r') as header_file:
        header = header_file.readline() + '\n'
    with open("OutputTemplates/InvoiceTemplate.txt", 'r') as inv_file:
        inv = inv_file.readline() + '\n'
    with open("OutputTemplates/ItemTemplate.txt", 'r') as item_file:
        item = item_file.readline() + '\n'
    with open("OutputTemplates/LabelTemplate.txt", 'r') as label_file:
        label = label_file.readline() + '\n'
    return header, inv, item, label

def output_item_string(template, item):
    """Returns a formatted string from the supplied template and invoice"""
    output = template.replace('Style', item.long_style)
    output = output.replace('UPC', item.UPC)
    output = output.replace('Qty', str(int(item.qty_each)))
    output = output.replace('Cost', str(item.unit_cost))
    output = output.replace('Color', item.color)
    output = output.replace('Size', item.size)
    output = output.replace('Desc', item.description)
    return output

def output_label_string(template, invoice):
    """Returns a formatted string from the supplied template and invoice"""
    output = template.replace('PO', invoice.purchase_order_number)
    output = output.replace('Store', invoice.store_number)
    output = output.replace('SSCC', invoice.SSCC)
    output = output.replace('Track', invoice.tracking_number)
    output = output.replace('Date', datetime.now().strftime("%Y%m%d"))
    output = output.replace('Dept', invoice.department_number)
    output = output.replace('Inv', invoice.invoice_number)
    output = output.replace('Add1', invoice.address1)
    output = output.replace('Add2', invoice.address2)
    output = output.replace('City', invoice.city)
    output = output.replace('State', invoice.state)
    output = output.replace('Zip', invoice.zip_code)
    output = output.replace('Qty', str(invoice.total_qty))
    output = output.replace('DC', invoice.distribution_center)
    output = output.replace('Name', str(invoice.store_name))
    return output

def get_sql_connection(conn_string):
    """
    Returns a pymssql connection object based on the connection string in settings.
    """
    conn_settings = get_conn_settings(conn_string)
    return pymssql.connect(conn_settings['SERVER'], conn_settings['UID'],
                           conn_settings['PWD'], conn_settings['DATABASE'])

def get_conn_settings(conn_string):
    """
    Returns a dictionary of connection settings from a given key=value, ;-delimited connection
    string
    """
    conn_list = [item.split('=') for item in conn_string.split(';')]
    return {item[0]: item[1] for item in conn_list}
