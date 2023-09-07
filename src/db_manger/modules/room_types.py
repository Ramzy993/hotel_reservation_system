
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship


base = declarative_base()


class RoomType(base):
    __tablename__ = 'room_types'

    id = Column(Integer, primary_key=True)
    sea_view = Column(Boolean, nullable=False)
    pool_view = Column(Boolean, nullable=False)
    description = Column(String)
    capacity = Column(Integer)
    price_per_night = Column(Integer)

    rooms = relationship("Room", back_populates="type")

    def __init__(self, sea_view, pool_view, description, capacity, price_per_night):
        self.sea_view = sea_view
        self.pool_view = pool_view
        self.description = description
        self.capacity = capacity
        self.price_per_night = price_per_night

    def to_json(self):
        return {
            "id": self.id,
            "sea_view": self.sea_view,
            "pool_view": self.pool_view,
            "description": self.description,
            "capacity": self.capacity,
            "price_per_night": self.price_per_night,
        }
