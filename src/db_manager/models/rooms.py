
from datetime import datetime

from sqlalchemy import Column, Integer, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from src.db_manager import Base


class Room(Base):
    __tablename__ = 'rooms'

    id = Column(Integer, primary_key=True)
    hotel_id = Column(Integer, ForeignKey('hotels.id'))
    type_id = Column(Integer, ForeignKey('room_types.id'))

    room_number = Column(Integer, nullable=False)
    floor_number = Column(Integer, nullable=False)
    is_active = Column(Boolean, nullable=False, default=False)
    is_clean = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, default=datetime.utcnow())
    updated_at = Column(DateTime, default=datetime.utcnow())

    hotel = relationship("Hotel", back_populates="rooms")
    room_type = relationship("RoomType", back_populates="rooms")
    reservations = relationship("Reservation", back_populates="room")

    def __init__(self, hotel_id, type_id, room_number, floor_number):
        self.hotel_id = hotel_id
        self.type_id = type_id
        self.room_number = room_number
        self.floor_number = floor_number

    def to_json(self):
        return {
            "id": self.id,
            "hotel_id": self.hotel_id,
            "type_id": self.type_id,
            "room_number": self.room_number,
            "floor_number": self.floor_number,
            "is_active": self.is_active,
            "is_clean": self.is_clean
        }


