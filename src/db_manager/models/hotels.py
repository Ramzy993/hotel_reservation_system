
from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.orm import relationship

from src.db_manager import Base
from src.db_manager.utils import HotelClass


class Hotel(Base):
    __tablename__ = 'hotels'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    class_ = Column(Enum(*HotelClass.list_values(), name="HotelClass"), nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    employees = relationship("Employee", back_populates="hotel")
    rooms = relationship("Room", back_populates="hotel")

    def __init__(self, name, address, class_: HotelClass):
        self.name = name
        self.address = address
        self.class_ = class_
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "address": self.address,
            "class": self.class_,
        }


