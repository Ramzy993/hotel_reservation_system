
from datetime import datetime

from sqlalchemy import Column, Integer, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship


base = declarative_base()


class Room(base):
    __tablename__ = 'rooms'

    id = Column(Integer, primary_key=True)
    hotel_id = Column(Integer, ForeignKey('hotels.id'))
    type_id = Column(Integer, ForeignKey('room_types.id'))

    room_number = Column(Integer, nullable=False)
    floor_number = Column(Integer, nullable=False)
    is_active = Column(Boolean, nullable=False)
    is_clean = Column(Boolean, nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    hotel = relationship("Hotel", back_populates="rooms")
    type_ = relationship("RoomType", back_populates="rooms")
    reservations = relationship("Reservation", back_populates="room")

    def __init__(self, hotel_id, type_id, room_number, floor_number):
        self.hotel_id = hotel_id
        self.type_id = type_id
        self.room_number = room_number
        self.floor_number = floor_number
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def to_json(self):
        return {
            "id": self.id,
            "hotel_id": self.hotel_id,
            "type_id": self.type_id,
            "room_number": self.room_number,
            "floor_number": self.floor_number,
        }


