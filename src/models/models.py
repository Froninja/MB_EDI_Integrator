from sqlalchemy import create_engine, Column, Integer, String, Numeric, DateTime, ForeignKey, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from src.helpers.config import read_config

settings = read_config('Config.yaml')

engine = create_engine(r'sqlite:///' + settings['File Paths']['PO Database File'])

Base = declarative_base()

class PurchaseOrder(Base):
    __tablename__ = 'PurchaseOrders'

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

    stores = relationship('Store', order_by=Store.store_number, back_populates='PurchaseOrder')
    #invoices

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
    purchase_order_id = Column(Integer, ForeignKey('PurchaseOrders.id'))

    purchase_order = relationship('PurchaseOrder', back_populates='Stores')
    #items
    #invoice

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

    #store
    #invoice

class Invoice(Base):
    __tablename__ = 'Invoices'

    id = Column(Integer, primary_key=True)
    invoice_number
    customer
    po_number
    dept_number
    store_numbr
    dc_number
    discount_code
    discount
    total_cost
    total_qty
    ship_date
    tracking_number
    sscc_number
    address_1
    address_2
    city_state_zip

    #items
    #purchaseorder