from sqlalchemy import Column, Integer, Numeric, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class AddressBook(Base):
    __tablename__ = "address_book"

    id = Column(Integer, primary_key=True, index=True)
    address = Column(String(300), nullable=False)
    latitude = Column(Numeric, nullable=False)
    longitude = Column(Numeric, nullable=False)
