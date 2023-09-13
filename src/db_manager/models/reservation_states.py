
from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship

from src.db_manager.utils import ReservationStatus
from src.db_manager import Base


class ReservationState(Base):
    __tablename__ = 'reservation_states'

    id = Column(Integer, primary_key=True)
    state = Column(Enum(*ReservationStatus.list_values(), name="ReservationStatus"))

    reservations = relationship("Reservation", back_populates="status")

    def __init__(self, state):
        self.state = state

    def to_json(self):
        return {
            "id": self.id,
            "state": self.state,
        }
