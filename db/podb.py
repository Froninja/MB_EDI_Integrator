import sqlite3
import pickle
from datetime import datetime, timedelta, date
from models.purchaseorder import PurchaseOrder, Store, Item

class PurchaseOrderDB(object):
    """
    This class allows conventient access to the Purchase Order database stored
    as a SQLite3 file. Methods generally exposed - query, querymany, queryfilters,
    update, insert - accept and return PurchaseOrder objects
    """
    def __init__(self, db_name):
        #self.settings = settings
        self.db = sqlite3.connect(db_name, detect_types=sqlite3.PARSE_DECLTYPES)
        self.db.row_factory = sqlite3.Row

    def make_po(self, row, cursor):
        """
        Returns a PurchaseOrder object for a given row in the DB after querying
        store and item tables
        """
        po = PurchaseOrder(row['ponum'], row['customer'])
        try:
            po.cancel_ship = datetime.strptime(row['canceldate'], '%Y-%m-%d')
        except (ValueError, EOFError):
            pass
        po.status = row['status']
        try:
            po.creation_date = datetime.strptime(row['createdate'], '%Y-%m-%d')
        except ValueError:
            pass
        po.discount = row['discount']
        po.dept = row['dept']
        po.label = row['label']
        po.shipped_cost = row['shippedcost']
        try:
            po.shipped_invs = pickle.loads(row['shippedinvs'])
        except (pickle.UnpicklingError, EOFError, ImportError):
            pass
        try:
            po.start_ship = datetime.strptime(row['startdate'], '%Y-%m-%d')
        except ValueError:
            pass
        po.total_cost = row['totalcost']
        rows = cursor.execute("""SELECT *
        FROM stores
        WHERE ponum=?""", (po.po_number,)).fetchall()
        for row in rows:
            store = Store(row['storenum'])
            store.shipped_cost = row['shippedcost']
            store.shipped_qty = row['shippedqty']
            store.total_qty = row['totalqty']
            if store.shipped_cost == store.total_cost and store.shipped_qty == store.total_qty:
                store.shipped = True
            item_rows = cursor.execute("""SELECT *
            FROM items
            WHERE ponum=? AND storenum=?""", (po.po_number, store.store_num)).fetchall()
            for irow in item_rows:
                item = Item(irow['UPC'])
                item.cost = irow['cost']
                item.style_num = irow['style']
                item.total_qty = irow['qty']
                store.items[item.UPC] = item
            store.total_cost = sum([item.cost * item.total_qty for item in store.items.values()])
            po.stores[store.store_num] = store
        po.total_cost = sum([store.total_cost for store in po.stores.values()])
        return po

    def query(self, po_num):
        """
        Returns a single PurchaseOrder object from the DB if the provided PO
        number exists in the DB
        """
        c = self.db.cursor()
        row = c.execute("""SELECT *
        FROM purchaseorders
        WHERE ponum=?""", (po_num,)).fetchone()
        if row != None:
            po = self.make_po(row, c)
            return po

    def querymany(self, po_list):
        """
        Returns a list of PurchaseOrder objects from the DB for the provided
        list of PO numbers if they exist in the DB
        """
        return_list = []
        for po in po_list:
            return_list.append(self.query(po))
        return return_list

    def queryfilters(self, **kwargs):
        """
        Kwargs: customer=customer name; date=days in the past; complete=bool
        Returns a list of PurchaseOrder objects containing all POs in the DB
        that meet the provided customer, date, and completion filters
        """
        c = self.db.cursor()
        rows = c.execute("""SELECT ponum
        FROM purchaseorders""").fetchall()
        po_list = self.querymany([row[0] for row in rows])
        counter = 0
        return_list = po_list[:]
        for po in po_list:
            if 'customer' in kwargs and po.customer != kwargs['customer']:
                return_list.remove(po)
            elif 'date' in kwargs:
                delta = timedelta(kwargs['date'])
                try:
                    if po.creation_date < datetime.today() - delta:
                        return_list.remove(po)
                except TypeError:
                    return_list.remove(po)
            #elif 'complete' in kwargs and po.complete != kwargs['complete']:
                #return_list.remove(po)
        return return_list

    def queryfilters(self, customer, days, status):
        """
        Returns a list of PurchaseOrder objects containing all POs in the DB
        that meet the provided customer, date, and status filters
        """
        c = self.db.cursor()
        if len(status) < 1:
            status = ['', None]
        sql = ('SELECT * FROM purchaseorders WHERE customer=? AND createdate>? AND status IN (%s)'
               % ','.join('?' * len(status)))
        params = [customer, (date.today() - timedelta(days)).strftime("%Y-%m-%d")] + status
        return_list = []
        for row in c.execute(sql, params).fetchall():
            return_list.append(self.make_po(row, c))
        return return_list

    def queryall(self):
        c = self.db.cursor()
        rows = c.execute("""SELECT ponum
        FROM purchaseorders""").fetchall()
        po_list = self.querymany([row[0] for row in rows])
        return po_list

    def update(self, po):
        """
        Updates all values for PO in the database with a PO number matching the
        provided PurchaseOrder object
        """
        c = self.db.cursor()
        c.execute("""UPDATE purchaseorders
        SET customer=?, createdate=?, startdate=?, canceldate=?, totalcost=?, discount=?, label=?, status=?, shippedcost=?, shippedinvs=?, dept=?
        WHERE ponum=?""",
                  (po.customer, po.creation_date.strftime("%Y-%m-%d"),
                   po.start_ship.strftime("%Y-%m-%d"), po.cancel_ship.strftime("%Y-%m-%d"),
                   po.total_cost, po.discount, po.label, po.status, po.shipped_cost,
                   pickle.dumps(po.shipped_invs), po.dept, po.po_number))
        for store in po.stores.values():
            c.execute("""UPDATE stores
            SET totalcost=?, totalqty=?, shippedcost=?, shippedqty=?
            WHERE ponum=? AND storenum=?""",
                      (store.total_cost, store.total_qty, store.shipped_cost,
                       store.shipped_qty, po.po_number, store.store_num))
            for item in store.items.values():
                c.execute("""UPDATE items
                SET style=?, cost=?, qty=?
                WHERE ponum=? AND storenum=? AND upc=?""",
                          (item.style_num, item.cost, item.total_qty,
                           po.po_number, store.store_num, item.UPC))
        self.db.commit()

    def insert(self, po):
        """
        Adds new records to the DB corresponding to the provide PurchaseOrder
        object
        """
        c = self.db.cursor()
        c.execute("INSERT INTO purchaseorders VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                  (po.po_number, po.customer, po.creation_date.strftime("%Y-%m-%d"), po.start_ship.strftime("%Y-%m-%d"), po.cancel_ship.strftime("%Y-%m-%d"),
                   po.total_cost, po.discount, po.label, po.status, po.shipped_cost, pickle.dumps(po.shipped_invs), po.dept))
        for store in po.stores.values():
            c.execute("INSERT INTO stores VALUES (?,?,?,?,?,?)",
                      (po.po_number, store.store_num, store.total_cost, store.total_qty,
                       store.shipped_cost, store.shipped_qty))
            for item in store.items.values():
                c.execute("INSERT INTO items VALUES (?,?,?,?,?,?,?)",
                          (po.po_number, store.store_num, item.UPC, item.style_num,
                           item.cost, item.total_qty, False))
        self.db.commit()

    def get_po_from_export(self):
        """
        Searches the export files provided by customer settings and adds the
        PurchaseOrders to the DB
        """
        for customer in self.settings['CustomerSettings']:
            print("Customer: %s" % customer['Name'])
            try:
                with open(self.settings['FilePaths']['PO Export File'], 'r') as export:
                    for line in export:
                        line = line.rstrip('\n').rstrip('\r').split(',')
                        print(line)
                        if line[1] != 'PO #':
                            print("OK")
                            if self.query(line[1].lstrip('0')) is None:
                                if self.get_customer_from_export(line[0]) != False:
                                    PO = PurchaseOrder(line[1].lstrip('0'), self.get_customer_from_export(line[0]))
                                    print("Adding PO# %s" % PO.po_number)
                                    PO.start_ship = datetime.strptime(line[2], "%m/%d/%Y")
                                    PO.cancel_ship = datetime.strptime(line[3], "%m/%d/%Y")
                                    PO.creation_date = datetime.strptime(line[10], "%Y/%m/%d")
                                    PO.dept = line[11]
                                    PO.get_items_from_export(customer.k_po_in_file)
                                    PO.get_stores_from_export(customer.k_po_in_file)
                                    for item in PO.items.values():
                                        PO.total_cost += (item.cost * item.total_qty)
                                    self.insert(PO)
                            else:
                                print("PO already in DB")
            except FileNotFoundError:
                print("Could not find file %s" % customer.k_po_in_file)
                
    def read_export(self, export_path):
        po_dict = dict()
        try:
            with open(export_path, 'r') as export:
                for line in export:
                    line = line.rstrip('\n').rstrip('r').split(',')
                    self._create_po(line, po_dict)
        except FileNotFoundError:
            print("Could not find file %s" % export_path)
        db_list = self.querymany(po_dict.keys())


    def _create_po(self, line, po_dict):
        if line[0] != 'T':
            if line[1].lstrip('0') not in po_dict:
                po = PurchaseOrder(line[1].lstrip('0'), self.get_customer_from_export(line[0]))
                print("Creating PO# %s" % po.po_number)
                po.start_ship = datetime.strptime(line[2], "%m/%d/%Y")
                po.cancel_ship = datetime.strptime(line[3], "%m/%d/%Y")
                po.creation_date = datetime.strptime(line[10], "%Y/%m/%d")
                po.dept = line[11]
                po_dict[po.po_number] = po
                self._add_store_to_po(line, po)
            else:
                po = po_dict[line[1].lstrip('0')]
                self._add_store_to_po(line, po)

    def _add_store_to_po(self, line, po):
        if line[4] not in po.stores:
            st = Store(line[4])
            print("Creating store# %s" % st.store_num)
            po.stores[st.store_num] = st
            self._add_item_to_store(line, st)
        else:
            st = po.stores[line[4]]
            self._add_item_to_store(line, st)

    def _add_item_to_store(self, line, store):
        if line[5] not in store.items:
            item = Item(line[5])
            print("Creating item with UPC #%s" % item.UPC)
            item.style_num = line[6]
            item.cost = line[7]
            item.total_qty = line[9]
            store.items[item.UPC] = item

    def get_customer_from_export(self, id):
        """
        Returns a customer matching the ID provided in the first field of the
        export file
        """
        print("ID from file: %s" % id.lstrip('0'))
        for customer in self.settings['CustomerSettings']:
            if id.lstrip('0') == str(customer['Attributes']['PO ID']):
                print("Found a match")
                return customer['Name']
            if id.lstrip() == customer['Attributes']['Invoice ID']:
                print("Found a match")
                return customer['Name']
        return False

    def fix_dates(self):
        """
        A console input function allowing the user to enter missing dates
        for all POs in the DB that have dates missing
        """
        for po in self.queryfilters():
            print(po.customer)
            print(po.po_number)
            if input() == 'q':
                return
            if po.start_ship == '' or po.start_ship is None:
                print("Enter start ship date")
                while True:
                    try:
                        date = datetime.strptime(input(), "%m/%d/%Y")
                        break
                    except ValueError:
                        print("Invalid format")
                po.start_ship = date
            if po.cancel_ship == '' or po.cancel_ship is None:
                print("Enter cancel ship date")
                while True:
                    try:
                        date = datetime.strptime(input(), "%m/%d/%Y")
                        break
                    except ValueError:
                        print("Invalid format")
                po.cancel_ship = date
            if po.creation_date == '' or po.creation_date is None:
                print("Enter creation date")
                while True:
                    try:
                        date = datetime.strptime(input(), "%m/%d/%Y")
                        break
                    except ValueError:
                        print("Invalid format")
                po.creation_date = date
            self.update(po)

    def convert_dates_to_ISO(self):
        for po in self.queryall():
            self.update(po)

if __name__ == '__main__':
    settings = dict()
    settings['po_db'] = 'PO_Database'
    db = PurchaseOrderDB(settings)
    db.convert_dates_to_ISO()
