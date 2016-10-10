class PurchaseOrder(object):
    """Holds all the relevant information for one purchase order.
        Information includes:
        - Purchase Order Number
        - Customer (who submitted the purchase order)
        - Creation Date (determined on customer end)
        - Start Ship Date
        - Cancel Date
        - Total Cost (sum of unit cost * qty for each item in the order)
        - Discount Requested (as a %)
        - Label (created on receiver end)
        - Completion Status (whether it has shipped or not)
        - Items"""
    def __init__(self, po_number, customer):
        self.po_number = po_number
        self.customer = customer
        self.creation_date = ''
        self.start_ship = ''
        self.cancel_ship = ''
        self.total_cost = 0
        self.discount = 0
        self.label = ''
        self.status = ''
        self.dept = ''
        self.items = dict()
        self.stores = dict()
        self.shipped_cost = 0
        self.shipped_invs = []

    def get_items_from_export(self, export_file):
        with open(export_file, 'r') as export:
            for line in export:
                line = line.rstrip('\n').rstrip('\r').split(',')
                if line[1].lstrip('0') == self.po_number:
                    if line[5] not in self.items:
                        item = Item(line[5])
                        item.cost = float(line[7])
                        item.style_num = line[6]
                        item.stores.append(line[4])
                        item.total_qty += float(line[9])
                        self.items[item.upc] = item
                    else:
                        item = self.items[line[5]]
                        item.stores.append(line[4])
                        item.total_qty += float(line[9])

    def get_stores_from_export(self, export_file):
        with open(export_file, 'r') as export:
            for line in export:
                line = line.rstrip('\n').rstrip('\r').split(',')
                if line[1].lstrip('0') == self.po_number:
                    if line [4] not in self.stores:
                        store = Store(line[4])
                        item = Item(line[5])
                        item.style_num = line[6]
                        item.cost = float(line[7])
                        item.total_qty = line[9]
                        store.items[item.upc] = item
                        store.total_cost += item.cost
                        store.total_qty += float(item.total_qty)
                        self.stores[store.store_num] = store
                    else:
                        store = self.stores[line[4]]
                        item = Item(line[5])
                        item.style_num = line[6]
                        item.cost = line[7]
                        item.total_qty = line[9]
                        store.items[item.upc] = item
                        store.total_cost += float(item.cost)
                        store.total_qty += float(item.total_qty)

class Item(object):
    def __init__(self, upc):
        self.upc = upc
        self.style_num = ''
        self.stores = []
        self.cost = 0
        self.total_qty = 0

    def __repr__(self):
        return "{0}: Cost: ${1}, Qty {2}\n".format(self.upc, self.cost,
                                                 self.total_qty)

class Store(object):
    def __init__(self, store_num):
        self.store_num = store_num
        self.items = dict()
        self.total_cost = 0
        self.total_qty = 0
        self.shipped_cost = 0
        self.shipped_qty = 0
        self.shipped = False

    """def __repr__(self):
        return_string = "{0}: Cost: ${1}, Qty {2}\n".format(self.store_num,
                                                          self.total_cost,
                                                          self.total_qty)
        for item in sorted(self.items.values(), key=lambda x: x.upc):
            return_string += item.__repr__()
        return return_string"""