from sqlalchemy import create_engine, Column, Integer, String, Numeric, DateTime, ForeignKey, func
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
    cost = Column(Numeric)
    retail = Column(Numeric)
    qty = Column(Integer)
    shipped_cost = Column(Numeric)
    shipped_retail = Column(Numeric)
    shipped_qty = Column(Integer)
    store_id = Column(Integer, ForeignKey('Stores.id'))
    invoice_id = Column(Integer, ForeignKey('Invoices.id'))

    store = relationship('Store', back_populates='items')
    invoice = relationship('Invoice', back_populates='items')

class Invoice(Base):
    __tablename__ = 'Invoices'

    id = Column(Integer, primary_key=True)
    invoice_number = Column(String)
    customer = Column(String)
    po_number = Column(String)
    dept_number = Column(String)
    store_numbr = Column(String)
    dc_number = Column(String)
    discount_code = Column(String)
    discount = Column(Integer)
    total_cost = Column(Numeric)
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

class Store(Base):
    __tablename__ = 'Stores'

    id = Column(Integer, primary_key=True)
    store_number = Column(String)
    dc_number = Column(String)
    total_cost = Column(Numeric)
    total_retail = Column(Numeric)
    total_qty = Column(Integer)
    shipped_cost = Column(Numeric)
    shipped_retail = Column(Numeric)
    shipped_qty = Column(Integer)
    order_id = Column(Integer, ForeignKey('Orders.id'))

    order = relationship('Order', back_populates='stores')
    items = relationship('Item', order_by=Item.style, back_populates='store',
                         cascade="all, delete")
    invoices = relationship('Invoice', order_by=Invoice.invoice_number, back_populates='store')

class Order(Base):
    __tablename__ = 'Orders'

    id = Column(Integer, primary_key=True)
    po_number = Column(String)
    customer = Column(String)
    dept_number = Column(String)
    label = Column(String)
    status = Column(String)
    total_cost = Column(Numeric)
    total_retail = Column(Numeric)
    total_qty = Column(Integer)
    shipped_cost = Column(Numeric)
    shipped_retail = Column(Numeric)
    shipped_qty = Column(Integer)
    create_date = Column(DateTime)
    start_date = Column(DateTime)
    cancel_date = Column(DateTime)

    stores = relationship("Store", order_by=Store.store_number,back_populates='order',
                          cascade="all, delete")
    invoices = relationship('Invoice', order_by=Invoice.invoice_number,
                            back_populates='order')
