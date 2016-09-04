from peewee import *
import yaml

def read_config(file_name):
    with open(file_name, 'r') as f:
        return yaml.load(f)

database = SqliteDatabase(read_config('Config.yaml')['File Paths']['PO Database File'])

class BaseModel(Model):
    class Meta:
        database = database

class PurchaseOrder(BaseModel):
    #Data derived from EDI 850:
    po_number = CharField()
    customer = CharField()
    dept = CharField()
    creation_date = DateField()
    start_ship = DateField()
    cancel_ship = DateField()
    total_cost = DecimalField()
    discount = IntegerField()
    #Data added by user:
    label = CharField()
    status = CharField()
    #Data added during shipping:
    shipped_cost = DecimalField()
    shipped_invs = BlobField()


class Store(BaseModel):
    purchase_order = ForeignKeyField(PurchaseOrder, related_name='stores',
                                     on_delete='cascade')
    #Data derived from EDI 850:
    store_num = CharField()
    total_cost = DecimalField()
    total_qty = IntegerField()
    #Data added during shipping:
    shipped_cost = DecimalField()
    shipped_qty = IntegerField()
    shipped = BooleanField()


class Item(BaseModel):
    store = ForeignKeyField(Store, related_name='items', on_delete='cascade')
    #Data derived from EDI 850:
    upc = CharField()
    style_num = CharField()
    cost = DecimalField()
    total_qty = IntegerField()


def create_tables():
    database.connect()
    database.create_tables([PurchaseOrder, Store, Item])
    database.close()


if __name__ == '__main__':
    import sqlite3
    from datetime import datetime
    try:
        PurchaseOrder.select()[0]
    except OperationalError:
        print("Creating Tables")
        create_tables()
    except IndexError:
        pass
    try:
        Store.select()[0]
    except IndexError:
        conn = sqlite3.connect('PO_Database')
        c = conn.cursor()
        c.execute("SELECT * FROM stores")
        database.connect()
        for row in c.fetchall():
            po = PurchaseOrder.select().where(PurchaseOrder.po_number == row[0]).get()
            store = Store(purchase_order=po,
                          store_num=row[1],
                          total_cost=row[2],
                          total_qty=row[3],
                          shipped_cost=row[4],
                          shipped_qty=row[5])
            if store.total_cost == store.shipped_cost:
                store.shipped = True
            else:
                store.shipped = False
            store.save()
        database.close()
    try:
        Item.select()[0]
        print("There are items")
    except IndexError:
        conn = sqlite3.connect('PO_Database')
        c = conn.cursor()
        c.execute("SELECT * FROM items")
        database.connect()
        for row in c.fetchall():
            query = (Store
                     .select()
                     .join(PurchaseOrder)
                     .where(PurchaseOrder.po_number == row[0] and Store.store_num == row[1]))
            st = query[0]
            item = Item(store=st,
                        upc=row[2],
                        style_num=row[3],
                        cost=row[4],
                        total_qty=row[5])
            item.save()
        database.close()