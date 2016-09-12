from sqlalchemy import create_engine, Column, Integer, String, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from src.helpers.config import read_config

settings = read_config('Config.yaml')

engine = create_engine(r'sqlite:///' + settings['File Paths']['PO Database File'])

Base = declarative_base()

class OutputRecord(Base):
    __tablename__ = 'OutputRecords'

    id = Column(Integer, primary_key=True)
    inv_num = Column(String)
    po_num = Column(String)
    store_num = Column(String)
    store_name = Column(String)
    dc_num = Column(String)
    dept_num = Column(String)
    total_qty = Column(Integer)
    ship_date = Column(DateTime, default=func.now())
    sscc = Column(String)
    tracking = Column(String)
    address1 = Column(String)
    address2 = Column(String)
    city_state_zip = Column(String)
