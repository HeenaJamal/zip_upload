# models.py
from sqlalchemy import Column, Integer, String, Float, Text, JSON, Table, MetaData
from database import Base

class CSVDataEntry(Base):
    __tablename__ = "csvdata_entries"
    id = Column(Integer, primary_key=True, index=True)
    column_name = Column(String, index=True)
    column_value = Column(Text, nullable=True)
