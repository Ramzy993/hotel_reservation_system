
from datetime import datetime

from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from src.db_manager import Base


class Reservation(Base):
    __tablename__ = 'reservations'

    id = Column(Integer, primary_key=True)
    room_id = Column(Integer, ForeignKey('rooms.id'))
    guest_id = Column(Integer, ForeignKey('guests.id'))
    employee_id = Column(Integer, ForeignKey('employees.id'))
    status_id = Column(Integer, ForeignKey('reservation_states.id'))

    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    balance = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow())
    updated_at = Column(DateTime, default=datetime.utcnow())

    room = relationship("Room", back_populates="reservations")
    guest = relationship("Guest", back_populates="reservations")
    employee = relationship("Employee", back_populates="reservations")
    status = relationship("ReservationState", back_populates="reservations")

    def __init__(self, room_id, guest_id, employee_id, status_id, start_date, end_date, balance):
        self.room_id = room_id
        self.guest_id = guest_id
        self.employee_id = employee_id
        self.status_id = status_id
        self.start_date = start_date
        self.end_date = end_date
        self.balance = balance

    def to_json(self):
        return {
            "id": self.id,
            "room_id": self.room_id,
            "guest_id": self.guest_id,
            "employee_id": self.employee_id,
            "status_id": self.status_id,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "balance": self.balance,
        }


