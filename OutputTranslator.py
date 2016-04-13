from Invoice import Invoice, Product
from PurchaseOrderDB import PurchaseOrderDB
from datetime import datetime, date, timedelta
from PyQt5 import QtWidgets, QtCore
from WarningDialogs import *
import time
import pymssql
import threading
import os.path

class ProgressThread(threading.Thread):
    def __init__(self, text):
        threading.Thread.__init__(self)
        self.p = ProgressDialog(text)

    def start(self):
        self.p.show()

class ProgressDialog(QtWidgets.QDialog):
    def __init__(self, text):
        QtWidgets.QDialog.__init__(self)
        self.layout = QtWidgets.QVBoxLayout(self)
        self.header = QtWidgets.QLabel(self)
        self.header.setText(text)
        self.header.setAlignment(QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.header)
        self.label = QtWidgets.QLabel(self)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.label)
        self.progress_bar = QtWidgets.QProgressBar(self)
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(17)
        self.progress_bar.setTextVisible(False)
        self.layout.addWidget(self.progress_bar)

    @QtCore.pyqtSlot(str, int)
    def update_progress(self, text, progress):
        self.setFocus()
        self.label.setText(text)
        self.progress_bar.setValue(progress)

class OutputTranslator(QtCore.QObject):
    """
    Single instance class to add requisite information and output for a list
    of invoices
    """
    progressed = QtCore.pyqtSignal(str, int)
    def __init__(self, customer, settings, append=False, test=False):
        QtCore.QObject.__init__(self)
        self.progress = 0
        self.customer = customer
        self.settings = settings
        self.invoice_list = []
        self.append = append
        self.test = test
        self.get_customer_settings()
        #if test:
            #self.p = ProgressDialog("Running Self-Test")
            #self.thread1 = ProgressThread("Running Self-Test")
        #else:
            #self.p = ProgressDialog("Processing")
            #self.thread1 = ProgressThread("Processing")
        #self.p.show()
        #self.progressed.connect(self.thread1.p.update_progress)
        #self.thread1.start()

    def initiate_db(self):
        self.po_db = PurchaseOrderDB(self.settings)

    def run(self, inv_array):
        self.generate_invoices(inv_array)
        if not self.get_ship_data():
            return False
        if not self.assign_destinations():
            return False
        self.assign_items()
        if not self.assign_upcs():
            return False
        if not self.po_in_db_check():
            return False
        if not self.store_and_item_checks():
            print("failed check")
            return False
        self.update_ship_status()
        return True

    def get_customer_settings(self):
        for customer in self.settings['customers']:
            if customer.a_name == self.customer:
                self.customer_settings = customer
                return

    def get_sql_connection(self):
        """
        Returns a pyodbc connection object based on the connection string in
        settings.
        """
        self.progress += 1
        return pymssql.connect("10.0.1.93", "amm", "amm", "LFL")

    def generate_invoices(self, inv_array):
        print("%s Starting invoice generation" % datetime.now())
        for row in inv_array:
            if len(row[0]) > 0:
                invoice = Invoice(row[0])
                invoice.purchase_order_number = row[1]
                invoice.discount(row[2])
                invoice.customer = self.customer
                invoice.get_dept_num(row[3], self.customer_settings.b_asset_dept, self.customer_settings.c_memo_dept)
                self.invoice_list.append(invoice)
                print("%s Created Invoice# %s, with PO# %s, Dept# %s, and discount %s" % (datetime.now(),
                                                                                          invoice.invoice_number,
                                                                                          invoice.purchase_order_number,
                                                                                          invoice.department_number,
                                                                                          invoice.discount_percent))
        self.invoice_list = sorted(sorted(self.invoice_list, key=lambda inv: inv.store_number),
                                   key=lambda inv: inv.purchase_order_number)
        print("%s Ending generation. Generated %s invoices" % (datetime.now(), len(self.invoice_list)))
        self.progress += 1
        
    def get_ship_data(self):
        print("%s Querying shipping info" % datetime.now())
        self.progressed.emit("Getting Shipping Info", self.progress)
        for invoice in self.invoice_list:
            invoice.shipping_information(self.settings['shiplog'])
            if invoice.tracking_number == '':
                self.w = TrackingWarningDialog(invoice.invoice_number)
                self.w.exec_()
                if self.w.confirmed == True:
                    invoice.tracking_number = self.w.tracking
                    invoice.shipping_information_from_tracking(self.settings['shiplog'])
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
        with self.get_sql_connection() as conn:
            with conn.cursor(as_dict=True) as cursor:
                min_date = date.today() - timedelta(365)
                sql = self.settings['destquery'].format(','.join(['%s'] * len(self.invoice_list)))
                params = [min_date] + [inv.invoice_number for inv in self.invoice_list]
                cursor.execute(sql, tuple(params))
                query_dict = dict()
                for row in cursor:
                    query_dict[str(row['NrDocF'])] = row
                sql = self.settings['memodestquery'].format(','.join(['%s'] * len(self.invoice_list)))
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
        with self.get_sql_connection() as conn:
            with conn.cursor(as_dict=True) as cursor:
                min_date = date.today() - timedelta(365)
                sql = self.settings['invquery'].format(','.join(['%s'] * len(self.invoice_list)))
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
        with self.get_sql_connection() as conn:
            with conn.cursor(as_dict=True) as cursor:
                query_dict = dict()
                if len(ring_list) > 0:
                    cursor.execute(self.settings['ringupcquery'].format(ring_list))
                    for row in cursor:
                        query_dict['{}-{}-{}-{}-{}'.format(row['CodMod'], row['Cod'], row['Colore'], row['Sup'], str(row['Inch']))] = row
                if len(non_ring_list) > 0:
                    cursor.execute(self.settings['upcquery'].format(non_ring_list))
                    for row in cursor:
                        query_dict['{}-{}-{}-{}-{}'.format(row['CodMod'], row['Cod'], row['Colore'], row['Sup'], str(row['Lgh']))] = row
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
                item = Product('{}-{}-{}-{}-{}'.format(row['codmod'], row['codpiet'], row['colore'], row['codsup'], str(row['lungh'])))
                item.qty_each = row['qtamov']
                item.unit_cost = row['valorev']/item.qty_each
                if self.customer_settings.d_desc_needed == 'True':
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
        with open(self.settings['desclog'], 'r') as desc_log:
            for line in desc_log:
                line = line.rstrip('\n').split(',')
                if line[0] == item.long_style:
                    item.description = line[1]
                    item.size = line[2]
                    item.color = line[3]
        if item.description == '':
            self.w = DescriptionWarningDialog(item.UPC, item.long_style, inv.invoice_number)
            self.w.exec_()
            if self.w.confirmed == True:
                item.description = self.w.description
                item.size = self.w.size
                item.color = self.w.color
                with open(self.settings['desclog'], 'a') as desc_log:
                    desc_log.write("%s,%s,%s,%s\n" % (item.long_style, item.description,
                                                      item.size, item.color))
        return item
        print("%s Descriptions assigned" % datetime.now())

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
            with open(self.settings['destlog'], 'r') as dest_log:
                for line in dest_log:
                    line = line.split(',')
                    if line[0] == invoice.customer and line[1] == str(mb_dest):
                        invoice.store_number = line[2].zfill(4)
                        invoice.distribution_center = line[3].zfill(4)
                        invoice.store_name = line[4].rstrip('\n').rstrip('\r')
            if invoice.store_number == '':
                self.w = StoreWarningDialog(mb_dest, invoice.invoice_number)
                self.w.exec_()
                if self.w.confirmed == True:
                    invoice.store_number = self.w.store_num
                    invoice.store_name = self.w.store_name
                    invoice.distribution_center = self.w.dc_num
                    with open(self.settings['destlog'], 'a') as dest_log:
                        dest_log.write("%s,%s,%s,%s,%s\n" % (invoice.customer, mb_dest, invoice.store_number,
                                                             invoice.distribution_center, invoice.store_name))
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
                    item.UPC_exception_check(self.settings['upcexceptlog'], invoice.customer)
                except KeyError:
                    item.UPC_exception_check(self.settings['upcexceptlog'], invoice.customer)
                if item.UPC == '' or item.UPC == None:
                    self.w = UPCWarningDialog(item.long_style, invoice.invoice_number)
                    self.w.exec_()
                    if self.w.confirmed == True:
                        item.UPC = self.w.UPC
                    else:
                        return False
        print("%s UPCs assigned" % datetime.now())
        self.progress += 1
        return True

    def po_in_db_check(self):
        print("%s Starting PO Check" % datetime.now())
        po_list = []
        for invoice in self.invoice_list:
            if invoice.purchase_order_number not in po_list:
                po_list.append(invoice.purchase_order_number)
        for po in po_list:
            if self.po_db.query(po) == None:
                print("PO# %s not in database" % po)
                self.w = POWarningDialog(po, [inv.invoice_number for inv in self.invoice_list if inv.purchase_order_number == po])
                self.w.exec_()
                if self.w.confirmed == True and len(self.w.po_num) > 0:
                    for inv in [inv for inv in self.invoice_list if inv.purchase_order_number == po]:
                        inv.purchase_order_number = self.w.po_num
                    self.po_in_db_check()
                elif self.w.confirmed == True:
                    continue
                else:
                    return False
        self.progress += 1
        return True
        

    def store_and_item_checks(self):
        for invoice in self.invoice_list:
            try:
                if not self.store_for_po_check(invoice):
                    return False
                invoice.po_create_date = self.po_db.query(invoice.purchase_order_number).creation_date
            except (KeyError, AttributeError):
                continue
        self.progress += 1
        return True

    def store_for_po_check(self, invoice):
        po = self.po_db.query(invoice.purchase_order_number)
        try:
            if invoice.store_number.zfill(4) in po.stores:
                store = po.stores[invoice.store_number.zfill(4)]
                for item in invoice.items:
                    if not self.item_for_store_check(item, store, invoice.invoice_number, po.po_number):
                        return False
                return True
            else:
                m = WarningDialog("Store# %s (invoice# %s) is not allocated on PO# %s"\
                    % (invoice.store_number, invoice.invoice_number, po.po_number))
                if m.exec_() == QtWidgets.QMessageBox.Cancel:
                    return False
                return True
        except AttributeError:
            return True

    def item_for_store_check(self, item, store, inv_num, po_num):
        if item.UPC in store.items:
            if self.item_qty_for_store_check(item, store, inv_num, po_num):
                return True
            else:
                return False
        else:
            detail_string = "Items on store# %s:\n" % store.store_num + "\n".join(["%s"] * len(store.items)) %\
                tuple([i.style_num + " | " + i.UPC for i in store.items.values()])
            m = WarningDialog("Style %s (UPC %s) on invoice# %s is not allocated to store# %s on PO# %s"\
                % (item.long_style, item.UPC, inv_num, store.store_num, po_num), detail=detail_string)
            if m.exec_() == QtWidgets.QMessageBox.Cancel:
                return False
            return True

    def item_qty_for_store_check(self, item, store, inv_num, po_num):
        if item.qty_each != float(store.items[item.UPC].total_qty):
            print("Calling warning dialog")
            m = WarningDialog("Qty of style %s on invoice# %s does not match qty for store# %s on PO# %s"\
                % (item.long_style, inv_num, store.store_num, po_num))
            if m.exec_() == QtWidgets.QMessageBox.Cancel:
                return False
            return True
        else:
            return True

    def update_ship_status(self):
        print("%s Updating shipping status" % datetime.now())
        for invoice in self.invoice_list:          
            po = self.po_db.query(invoice.purchase_order_number)
            if po != None:
                if invoice.invoice_number not in [inv.invoice_number for inv in po.shipped_invs]:
                    po.shipped_invs.append(invoice)
                    po.shipped_cost += invoice.total_cost
                    try:                    
                        store = po.stores[invoice.store_number.zfill(4)]
                        store.shipped_cost += invoice.total_cost
                        store.shipped_qty += invoice.total_qty
                        if store.shipped_cost >= store.total_cost:
                            store.shipped = True
                    except:
                        print("Store error")
                        print(invoice.store_number)
                        print([store.store_num for store in po.stores.values()])
                self.po_db.update(po)
        self.progress += 1
        print(self.progress)
        #if self.test:
            #self.p.close()

    def check_for_existing_file(self):
        if os.path.isfile(self.settings['mapdata'] + self.customer_settings.j_ship_out_file)\
            or os.path.isfile(self.settings['mapdata'] + self.customer_settings.i_inv_out_file):
            return True
        else:
            return False

    def write_output(self):
        print("%s Beginning Output" % datetime.now())
        header_temp, inv_temp, item_temp, label_temp = self.get_output_templates()
        if self.check_for_existing_file():
            m = OverWriteDialog()
            if m.exec_() == QtWidgets.QMessageBox.Yes:
                self.append = True
        if self.append == False:
            output_string = self.output_header_string(header_temp)
            mode = 'w'
        else:
            output_string = ''
            mode = 'a'
        label_string = ''
        for invoice in self.invoice_list:
            label_string += self.output_label_string(label_temp, invoice)
            output_string += self.output_inv_string(inv_temp, invoice)
            for item in invoice.items:
                output_string += self.output_item_string(item_temp, item)
        with open(self.settings['mapdata'] + self.customer_settings.j_ship_out_file, mode) as file:
            file.write(output_string)
        with open(self.settings['mapdata'] + self.customer_settings.i_inv_out_file, mode) as file:
            file.write(output_string)
        with open(self.settings['outputlog'],'a') as file:
            file.write(label_string)
        print("%s Output successful" % datetime.now())
        self.progress += 1
        self.progressed.emit("Output Complete", self.progress)

    def get_output_templates(self):
        with open("OutputTemplates/HeaderTemplate.txt",'r') as header_file:
            header = header_file.readline() + '\n'
        with open("OutputTemplates/InvoiceTemplate.txt",'r') as inv_file:
            inv = inv_file.readline() + '\n'
        with open("OutputTemplates/ItemTemplate.txt",'r') as item_file:
            item = item_file.readline() + '\n'
        with open("OutputTemplates/LabelTemplate.txt",'r') as label_file:
            label = label_file.readline() + '\n'
        return header, inv, item, label

    def output_header_string(self, template):
        output = template.replace('ReceiverInvID', self.customer_settings.f_inv_edi_id)
        output = output.replace('ReceiverShipID', self.customer_settings.g_ship_edi_id)
        output = output.replace('VersionNum', ('00' + self.customer_settings.h_edi_version)[:5])
        return output

    def output_inv_string(self, template, invoice):
        output = template.replace('Inv', invoice.invoice_number)
        output = output.replace('Store', invoice.store_number)
        output = output.replace('Track', invoice.tracking_number)
        try:
            output = output.replace('ShipDate', invoice.ship_date.strftime('%Y%m%d'))
        except:
            output = output.replace('ShipDate', datetime.now().strftime('%Y%m%d'))
        output = output.replace('DiscCode', invoice.discount_code)
        output = output.replace('Disc', str(invoice.discount_percent))
        output = output.replace('SSCC', invoice.SSCC)
        output = output.replace('PO', invoice.purchase_order_number)
        output = output.replace('Dept', invoice.department_number)
        output = output.replace('DC', invoice.distribution_center)
        output = output.replace('Qty', str(invoice.total_qty))
        if self.customer_settings.e_create_date_needed == True:
            output = output.replace('CreateDate', invoice.po_create_date.strftime("%Y/%m/%d"))
        else:
            output = output.replace('CreateDate', '')
        return output

    def output_item_string(self, template, item):
        output = template.replace('Style', item.long_style)
        output = output.replace('UPC', item.UPC)
        output = output.replace('Qty', str(int(item.qty_each)))
        output = output.replace('Cost', str(item.unit_cost))
        #output = output.replace('SecondStyle', item.proper_style)
        output = output.replace('Color', item.color)
        output = output.replace('Size', item.size)
        output = output.replace('Desc', item.description)
        return output

    def output_label_string(self, template, invoice):
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