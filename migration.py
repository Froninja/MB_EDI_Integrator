from src.models import models
from src.db.podb import PurchaseOrderDB
import sqlalchemy

old_db = PurchaseOrderDB('PO_Database')
new_db = sqlalchemy.orm.sessionmaker(bind=models.engine)()

for old_po in old_db.queryall():
    order = models.Order(po_number=old_po.po_number,
                         customer=old_po.customer,
                         dept_number=old_po.dept,
                         label=old_po.label,
                         status=old_po.status,
                         total_cost=old_po.total_cost,
                         shipped_cost=old_po.shipped_cost,
                         create_date=old_po.creation_date,
                         start_date=old_po.start_ship,
                         cancel_date=old_po.cancel_ship,
                         total_retail=0,
                         total_qty=0)
    for store_old in old_po.stores.values():
        store = models.Store(store_number=store_old.store_num,
                             total_cost=store_old.total_cost,
                             total_retail=0,
                             total_qty=store_old.total_qty,
                             shipped_cost=store_old.shipped_cost,
                             shipped_qty=store_old.shipped_qty)
        for item_old in store_old.items.values():
            item = models.Item(upc=item_old.upc,
                               style=item_old.style_num,
                               cost=item_old.cost,
                               retail=0,
                               qty=item_old.total_qty)
            store.items.append(item)
        order.stores.append(store)
    new_db.add(order)

new_db.commit()