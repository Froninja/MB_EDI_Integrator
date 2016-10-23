from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from src.helpers.config import read_config

settings = read_config('Config.yaml')

engine = create_engine(r'sqlite:///' + settings['File Paths']['PO Database File'])

Base = declarative_base()

class Item(Base):
    __tablename__ = 'Items'

    id = Column(Integer, primary_key=True)
    upc = Column(String)
    style = Column(String)
    cost = Column(Float)
    retail = Column(Float)
    qty = Column(Integer)
    shipped_cost = Column(Float)
    shipped_retail = Column(Float)
    shipped_qty = Column(Integer)
    store_id = Column(Integer, ForeignKey('Stores.id'))
    invoice_id = Column(Integer, ForeignKey('Invoices.id'))

    store = relationship('Store', back_populates='items')
    invoice = relationship('Invoice', back_populates='items')

    def __repr__(self):
        return ("Item: UPC " + self.upc + ", style " + str(self.style) + ", cost: $"
                + str(int(self.cost)) + ", retail: $" + str(int(self.retail)) + ", qty: "
                + str(self.qty))

class Invoice(Base):
    __tablename__ = 'Invoices'

    id = Column(Integer, primary_key=True)
    invoice_number = Column(String)
    customer = Column(String)
    po_number = Column(String)
    dept_number = Column(String)
    store_number = Column(String)
    store_name = Column(String)
    dc_number = Column(String)
    discount_code = Column(String)
    discount = Column(Integer)
    total_cost = Column(Float)
    total_qty = Column(Integer)
    ship_date = Column(DateTime)
    tracking_number = Column(String)
    sscc_number = Column(String)
    address_1 = Column(String)
    address_2 = Column(String)
    city_state_zip = Column(String)
    store_id = Column(Integer, ForeignKey('Stores.id'))
    order_id = Column(Integer, ForeignKey('Orders.id'))

    items = relationship('Item', order_by=Item.style, back_populates='invoice',
                         cascade="all, delete")
    order = relationship('Order', back_populates='invoices')
    store = relationship('Store', back_populates='invoices')

    def discount(self, discount_percent):
        """Sets the discount value and EDI discount code based on the provided value"""
        if discount_percent is None:
            self.discount = 0
        elif int(discount_percent) >= 0:
            self.discount = int(discount_percent)
        if discount_percent is None or int(discount_percent) == 0:
            self.discount_code = "05"
        else:
            self.discount_code = "08"

    def dept_number(self, memo_val, asset_dept, memo_dept):
        """Sets the department number based on the settings provided"""
        if memo_val is True or memo_val == 2:
            self.dept_number = memo_dept.zfill(4)
        else:
            self.dept_number = asset_dept.zfill(4)

    def get_totals(self):
        self.total_cost = sum([item.cost * item.qty for item in self.items])
        self.total_qty = sum([item.qty for item in self.items])

    def __repr__(self):
        return ("Invoice: " + self.invoice_number + ": for " + self.customer + " on PO #"
                + str(self.po_number) + "; shipped on " + str(self.ship_date) + " with tracking #"
                + str(self.tracking_number) + " and SSCC " + str(self.sscc_number) + "; total qty: "
                + str(self.total_qty) + ", total cost: " + str(self.total_cost) + "; to store #"
                + str(self.store_number) + " (" + str(self.store_name) + ") " + str(self.address_1)
                + ", " + str(self.address_2) + ", " + str(self.city_state_zip))

class Store(Base):
    __tablename__ = 'Stores'

    id = Column(Integer, primary_key=True)
    store_number = Column(String)
    dc_number = Column(String)
    total_cost = Column(Float)
    total_retail = Column(Float)
    total_qty = Column(Integer)
    shipped_cost = Column(Float)
    shipped_retail = Column(Float)
    shipped_qty = Column(Integer)
    order_id = Column(Integer, ForeignKey('Orders.id'))

    order = relationship('Order', back_populates='stores')
    items = relationship('Item', order_by=Item.style, back_populates='store',
                         cascade="all, delete")
    invoices = relationship('Invoice', order_by=Invoice.invoice_number, back_populates='store')

    def __repr__(self):
        return ("Store: store #" + self.store_number + ", DC #" + str(self.dc_number) + ", cost $"
                + str(int(self.total_cost)) + ", retail: $" + str(int(self.total_retail)) + ", qty: "
                + str(self.total_qty))

class Order(Base):
    __tablename__ = 'Orders'

    id = Column(Integer, primary_key=True)
    po_number = Column(String)
    customer = Column(String)
    dept_number = Column(String)
    label = Column(String)
    status = Column(String)
    total_cost = Column(Float)
    total_retail = Column(Float)
    total_qty = Column(Integer)
    shipped_cost = Column(Float)
    shipped_retail = Column(Float)
    shipped_qty = Column(Integer)
    create_date = Column(DateTime)
    start_date = Column(DateTime)
    cancel_date = Column(DateTime)

    stores = relationship("Store", order_by=Store.store_number,back_populates='order',
                          cascade="all, delete")
    invoices = relationship('Invoice', order_by=Invoice.invoice_number,
                            back_populates='order')

    def total(self):
        for store in self.stores:
            store.total_cost = sum([item.cost for item in store.items])
            store.total_retail = sum([item.retail for item in store.items])
            store.total_qty = sum([item.qty for item in store.items])
        self.total_cost = sum([store.total_cost for store in self.stores])
        self.total_retail = sum([store.total_retail for store in self.stores])
        self.total_qty = sum([store.total_qty for store in self.stores])

    def __repr__(self):
        return ("Order: PO #" + str(self.po_number) + ", customer: " + str(self.customer)
                + ", department #" + str(self.dept_number) + ", cost: $" + str(int(self.total_cost))
                + ", retail: $" + str(int(self.total_retail)) + ", qty: " + str(self.total_qty)
                + " units, created on " + str(self.create_date) + ", starting on "
                + str(self.start_date) + ", cancelling on " + str(self.cancel_date))
