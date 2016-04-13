import sqlite3
import pickle
from PODatabase import PODatabase

def create_tables(c):
    c.execute("""
    CREATE TABLE purchaseorders
    (ponum text, customer text, createdate text, startdate text, canceldate text, totalcost real, discount integer, label text, complete integer, shippedcost real, shippedinvs blob)
    """)
    c.execute("""
    CREATE TABLE stores
    (ponum text, storenum text, totalcost real, totalqty integer, shippedcost real, shippedqty integer)
    """)
    c.execute("""
    CREATE TABLE items
    (ponum text, storenum text, upc text, style text, cost real, qty integer, shipped integer)
    """)

po_db = PODatabase('r')

new_db = sqlite3.connect('PO_Database')
c = new_db.cursor()

create_tables(c)

po_count = 0
store_count = 0
item_count = 0
for po in po_db.purchase_orders.values():
    print("Entering PO# %s" % po.po_number)
    c.execute("INSERT INTO purchaseorders VALUES (?,?,?,?,?,?,?,?,?,?,?)",
              (po.po_number, po.customer, po.creation_date, po.start_ship, po.cancel_ship,
               po.total_cost, po.discount, po.label, po.complete, po.shipped_cost, pickle.dumps(po.shipped_invs)))
    po_count += 1
    for store in po.stores.values():
        print("Entering store# %s" % store.store_num)
        c.execute("INSERT INTO stores VALUES (?,?,?,?,?,?)",
                  (po.po_number, store.store_num, store.total_cost, store.total_qty,
                   store.shipped_cost, store.shipped_qty))
        store_count += 1
        for item in store.items.values():
            print("Entering item# %s" % item.UPC)
            c.execute("INSERT INTO items VALUES (?,?,?,?,?,?,?)",
                      (po.po_number, store.store_num, item.UPC, item.style_num, item.cost, item.total_qty, False))
            item_count += 1

print("Entered %s POs" % po_count)
print("Entered %s stores" % store_count)
print("Entered %s items" % item_count)

new_db.commit()

c.execute("SELECT * FROM purchaseorders")
for row in c:
    print(row)