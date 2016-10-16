import csv
from src.models.models import Order, Store, Item

class ExportReader(object):
    """Responsible for reading a structured flat file export and updating the Sqlite
    database with the resulting Order objects"""
    settings = dict()
    orders = dict()

    def __init__(self):
        pass

    def run(self):
        with open(self.settings['File Paths']['PO Export File']) as export:
            export_reader = csv.reader(export)
            for row in export_reader:
                if not is_header_row(row):
                    item = create_item(row)
                    order = check_for_order(row, self.orders)
                    if order:
                        store = check_for_store(row, order)
                        if not store:
                            store = create_store(row)
                            order.stores.append(store)
                        store.items.append(item)
                    
                        


def is_header_row(row):
    """Returns True if the row is a header row (containing no data)"""
    return row[1] == "PO #"

def create_item(row):
    """Returns a new Item using values from the row"""
    item = Item(style=row[6],
                upc=row[5],
                cost=row[7],
                qty=row[9])

    return item

def check_for_order(row, orders):
    """Returns an Order if that Order already exists in the orders dictionary. Otherwise, returns
    False"""
    if row[1].lstrip('0') not in orders:
        return False
    else:
        return orders[row[1].lstrip('0')]

def check_for_store(row, order):
    """Returns a Store if that Store has already been created for the Order. Otherwise, returns
    False"""
    if row[4] not in [store.store_number for store in order.stores]:
        return False
    else:
        return [store for store in order.stores where store.store_number == row[4]][0]

def create_store(row):
    store = Store(store_number=row[4])

    return store

def create_order(row):
    order = Order()

    return order