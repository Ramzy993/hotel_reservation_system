
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship

from src.db_manger.utils import ReservationStatus

base = declarative_base()


class ReservationState(base):
    __tablename__ = 'reservation_states'

    id = Column(Integer, primary_key=True)
    state = Column(String)

    reservations = relationship("Reservation", back_populates="status")

    def __init__(self, state: ReservationStatus):
        self.state = state

    def to_json(self):
        return {
            "id": self.id,
            "state": self.state,
        }
