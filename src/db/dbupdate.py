import csv
from datetime import datetime
from src.db.db import get_session
from src.helpers.config import read_config
from src.models.models import Order, Store, Item

class ExportReader(object):
    """Responsible for reading a structured flat file export and updating the Sqlite
    database with the resulting Order objects"""
    settings = dict()
    orders = dict()

    def __init__(self):
        self.settings = read_config('Config.yaml')
        self.database = get_session(self.settings['File Paths']['PO Databse File'])

    def collect_orders(self):
        with open(self.settings['File Paths']['PO Export File']) as export:
            export_reader = csv.reader(export)
            for row in export_reader:
                if not is_header_row(row):
                    item = create_item(row)
                    order = check_for_order(row, self.orders)
                    if not order:
                        order = new_order(row, self.settings, item)
                        self.orders[order.po_number] = order
                    else:
                        store = check_for_store(row, order)
                        if not store:
                            store = create_store(row)
                            order.stores.append(store)
                        store.items.append(item)
        for order in self.orders.values():
            order.total()
            print(stringify_order(order))

    def check_orders(self):
        self.database.query(Order).filter()



def is_header_row(row):
    """Returns True if the row is a header row (containing no data)"""
    return row[1] == "PO #"

def create_item(row):
    """Returns a new Item using values from the row"""
    item = Item(style=row[6],
                upc=row[5],
                cost=float(row[7]),
                retail=float(row[8]),
                qty=int(row[9]))
    return item

def check_for_order(row, orders):
    """Returns an Order if that Order already exists in the orders dictionary. Otherwise, returns
    False"""
    if row[1].lstrip('0') not in orders.keys():
        return False
    else:
        return orders[row[1].lstrip('0')]

def check_for_store(row, order):
    """Returns a Store if that Store has already been created for the Order. Otherwise, returns
    False"""
    if row[4] not in [store.store_number for store in order.stores]:
        return False
    else:
        return list(filter(lambda x: x.store_number == row[4], order.stores))[0]

def new_order(row, settings, item):
    """Returns a new order with a store and the item from the row"""
    order = create_order(row, settings)
    store = create_store(row)
    store.items.append(item)
    order.stores.append(store)
    return order

def create_store(row):
    """Returns a new store using values from the row"""
    store = Store(store_number=row[4])
    return store

def create_order(row, settings):
    """Returns a new order using values from the row"""
    order = Order(customer=find_customer(row, settings),
                  po_number=row[1].lstrip('0'),
                  dept_number=row[11],
                  start_date=datetime.strptime(row[2],'%m/%d/%Y'),
                  cancel_date=datetime.strptime(row[3],'%m/%d/%Y'),
                  create_date=datetime.strptime(row[10],'%Y/%m/%d'))
    return order

def find_customer(row, settings):
    return [customer['Name']
            for customer in settings['Customer Settings'].values()
            if customer['PO ID'] == row[0]][0]

def stringify_order(order):
    order_string = order.__repr__()
    for store in order.stores:
        order_string += '\n' + store.__repr__()
        for item in store.items:
            order_string += '\n' + item.__repr__()
    return order_string

def compare_orders(first_order, second_order):
    return stringify_order(first_order) == stringify_order(second_order)
