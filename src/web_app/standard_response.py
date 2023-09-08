import json
import datetime

from src.db_manager.models.employee_types import UserType
from src.db_manager.models.employees import Employee
from src.db_manager.models.guests import Guest
from src.db_manager.models.hotels import Hotel
from src.db_manager.models.reservations import Reservation
from src.db_manager.models.reservation_states import ReservationState
from src.db_manager.models.room_types import RoomType
from src.db_manager.models.rooms import Room


def default_serializer(obj):
    if isinstance(obj, (UserType, Employee, Guest, Hotel, Reservation, ReservationState, RoomType, Room)):
        return obj.to_json()
    elif type(obj) is datetime.datetime:
        return obj.strftime("%d-%b-%Y %H:%M:%S")

    raise Exception(f"Can not serialize: {str(type(obj))}")


def serializer(data, indent=4):
    return json.dumps(data, default=default_serializer, indent=indent)


class StandardResponse:

    def __init__(self, data, status):
        self.data = data
        self.status = status

    def to_json(self):
        return serializer({"data": self.data}), self.status

