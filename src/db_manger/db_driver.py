"""This module implements database driver for the system."""

import os
from datetime import datetime, timedelta
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.engine import URL


from src.common.logger import LogHandler
from src.common.config_manager import ConfigManager
from src.common.base_exception import HRSBaseException
from src.common.singleton import SingletonMeta

from src.db_manger.modules.guests import Guest
from src.db_manger.modules.employees import Employee
from src.db_manger.modules.employee_types import EmployeeType
from src.db_manger.modules.hotels import Hotel
from src.db_manger.modules.rooms import Room
from src.db_manger.modules.room_types import RoomType
from src.db_manger.modules.reservations import Reservation
from src.db_manger.modules.reservation_states import ReservationState


from src.db_manger.utils import EmployeeRole, RolePermissions, ReservationStatus, HotelClass


base = declarative_base()
logger = LogHandler().logger


ACCESS_TOKEN_EXPIRATION_HOURS = ConfigManager().get_str('JWT', 'jwt_access_token_expiration_hours')


class DatabaseDriverException(HRSBaseException):
    """
    this class is used to raise exception related to database
    """


class DBDriver(metaclass=SingletonMeta):

    def __init__(self):
        super().__init__()
        self.dialect = ConfigManager().get_str('DATABASE', 'dialect', fallback='sqlite')
        self.database_name = ConfigManager().get_str('DATABASE', 'database_name')
        self.host = ConfigManager().get_str('DATABASE', 'host')
        self.port = ConfigManager().get_str('DATABASE', 'port')
        self.username = ConfigManager().get_str('DATABASE', 'username')
        self.password = ConfigManager().get_str('DATABASE', 'password')

        if self.dialect == 'sqlite':
            if not os.path.isdir('tmp'):
                os.makedirs('tmp')
            self.connection_string = self.dialect + ":///tmp/" + self.database_name + '.db'
        else:
            self.connection_string = URL.create(username=self.username, host=self.host, port=self.port,
                                                drivername=self.dialect, database=self.database_name,
                                                password=self.password)

        self.engine = create_engine(self.connection_string)

        base.metadata.create_all(self.engine)

        self.connection = self.engine.connect()
        logger.info("connected to database")

        self.session = sessionmaker(bind=self.engine)()

        self.__seed_db()

    def __del__(self):
        self.connection.close()
        logger.info("disconnected from database")

    def __seed_db(self):
        for state in ReservationStatus.list_values():
            if not self.get_reservation_states(state=state):
                self.create_reservation_state(state)

        employee_types = self.get_employee_types(role=EmployeeRole.ADMIN.value)
        if len(employee_types) == 0:
            employee_types = self.create_employee_type(EmployeeRole.ADMIN.value, RolePermissions.list_values())

        admin_username = ConfigManager().get_str('ADMIN', 'username')
        admin_password = ConfigManager().get_str('ADMIN', 'password')
        admin_email = ConfigManager().get_str('ADMIN', 'email')

        admin = (self.get_employees(username=admin_username) or [None])[0]

        if admin is None:
            self.create_employee(employee_type_id=employee_types[0].id, username=admin_username, password=admin_password,
                                 email=admin_email, name="admin", staff_number=1, hotel_id=None)

    def __commit(self, records):
        try:
            if isinstance(records, list):
                self.session.add_all(records)
            else:
                self.session.add(records)
            self.session.commit()
        except Exception as e:
            logger.error(f"Database Error: {e}")
            self.session.rollback()

    def __dynamic_filter(self, model, args_dict):
        if model is None:
            raise DatabaseDriverException("cannot find model")

        args_dict.pop('self')

        query = self.session.query(model)
        model_attr_dict = vars(model)

        for key, value in args_dict.items():
            if value is not None and key in model_attr_dict:
                attr = getattr(model, key)
                query = query.filter(attr == value)

        return query

    def __dynamic_update(self, model, args_dict):
        if model is None:
            raise DatabaseDriverException("cannot find model")

        args_dict.pop('self')
        args_dict.pop('id', None)

        model_attr_dict = vars(model)

        for key, value in args_dict.items():
            if value is not None and key in model_attr_dict:
                setattr(model, key, value)

        return model

    def create_employee(self, hotel_id, employee_type_id, staff_number, name, username, password, email):
        try:
            employee = Employee(hotel_id=hotel_id, employee_type_id=employee_type_id, staff_number=staff_number,
                                username=username, password=password, name=name, email=email)
            self.__commit(employee)
            return employee

        except Exception as e:
            raise DatabaseDriverException(f"Database ERROR: {e}")

    def get_employees(self, id=None, hotel_id=None, employee_type_id=None, staff_number=None, name=None, username=None,
                      email=None):
        try:
            employees = self.__dynamic_filter(Employee, locals()).all()
            return employees

        except Exception as e:
            raise DatabaseDriverException(f"Database ERROR: {e}")

    def update_employee(self, id, hotel_id=None, employee_type_id=None, staff_number=None, name=None, username=None,
                        email=None, logged_in=None):
        try:
            employee = self.session.query(Employee).filter_by(id=id).first()
            employee = self.__dynamic_update(Employee, locals())
            self.session.commit()
            return employee

        except Exception as e:
            raise DatabaseDriverException(f"Database ERROR: {e}")

    def update_employee_token(self, id, user_token):
        try:
            employee = self.session.query(Employee).filter_by(id=id).first()
            employee = self.__dynamic_update(Employee, locals())
            employee.set_token_expiration(datetime.utcnow() + timedelta(hours=ACCESS_TOKEN_EXPIRATION_HOURS))
            self.session.commit()
            return employee

        except Exception as e:
            raise DatabaseDriverException(f"Database ERROR: {e}")

    def delete_employee(self, id):
        try:
            self.session.query(Employee).filter_by(id=id).delete()
            self.session.commit()

        except Exception as e:
            self.session.rollback()
            raise DatabaseDriverException(f"Database ERROR: {e}")

    def create_employee_type(self, role: EmployeeRole, permissions: list[RolePermissions]):
        try:
            employee_type = EmployeeType(role=role, permissions=permissions)
            self.__commit(employee_type)
            return employee_type

        except Exception as e:
            raise DatabaseDriverException(f"Database ERROR: {e}")

    def get_employee_types(self, id=None, role=None):
        try:
            employee_types = self.__dynamic_filter(EmployeeType, locals()).all()
            return employee_types

        except Exception as e:
            raise DatabaseDriverException(f"Database ERROR: {e}")

    def update_employee_type_permission(self, id, permissions: list[RolePermissions]):
        try:
            permissions = [permission.value for permission in permissions]
            employee_type = self.session.query(EmployeeType).filter_by(id=id).first()
            employee_type = self.__dynamic_update(EmployeeType, locals())
            self.session.commit()
            return employee_type

        except Exception as e:
            raise DatabaseDriverException(f"Database ERROR: {e}")

    def delete_employee_type(self, id):
        try:
            self.session.query(EmployeeType).filter_by(id=id).delete()
            self.session.commit()

        except Exception as e:
            self.session.rollback()
            raise DatabaseDriverException(f"Database ERROR: {e}")

    def create_guest(self, name, username, password, email):
        try:
            guest = Guest(username=username, password=password, name=name, email=email)
            self.__commit(guest)
            return guest

        except Exception as e:
            raise DatabaseDriverException(f"Database ERROR: {e}")

    def get_guests(self, id=None, name=None, username=None, email=None):
        try:
            guests = self.__dynamic_filter(Guest, locals()).all()
            return guests

        except Exception as e:
            raise DatabaseDriverException(f"Database ERROR: {e}")

    def update_guest(self, id, name=None, username=None, email=None, logged_in=None):
        try:
            guest = self.session.query(Guest).filter_by(id=id).first()
            guest = self.__dynamic_update(Guest, locals())
            self.session.commit()
            return guest

        except Exception as e:
            raise DatabaseDriverException(f"Database ERROR: {e}")

    def update_guest_token(self, id, user_token):
        try:
            guest = self.session.query(Guest).filter_by(id=id).first()
            guest = self.__dynamic_update(Guest, locals())
            guest.set_token_expiration(datetime.utcnow() + timedelta(hours=ACCESS_TOKEN_EXPIRATION_HOURS))
            self.session.commit()
            return guest

        except Exception as e:
            raise DatabaseDriverException(f"Database ERROR: {e}")

    def delete_guest(self, id):
        try:
            self.session.query(Guest).filter_by(id=id).delete()
            self.session.commit()

        except Exception as e:
            self.session.rollback()
            raise DatabaseDriverException(f"Database ERROR: {e}")

    def create_hotel(self, name, address, class_: HotelClass):
        try:
            hotel = Hotel(name=name, address=address, class_=class_.value)
            self.__commit(hotel)
            return hotel

        except Exception as e:
            raise DatabaseDriverException(f"Database ERROR: {e}")

    def get_hotels(self, id=None, name=None, class_=None):
        try:
            hotels = self.__dynamic_filter(Hotel, locals()).all()
            return hotels

        except Exception as e:
            raise DatabaseDriverException(f"Database ERROR: {e}")

    def update_hotel(self, id, name=None, address=None, class_=None):
        try:
            hotel = self.session.query(Hotel).filter_by(id=id).first()
            hotel = self.__dynamic_update(Hotel, locals())
            self.session.commit()
            return hotel

        except Exception as e:
            raise DatabaseDriverException(f"Database ERROR: {e}")

    def delete_hotel(self, id):
        try:
            self.session.query(Hotel).filter_by(id=id).delete()
            self.session.commit()

        except Exception as e:
            self.session.rollback()
            raise DatabaseDriverException(f"Database ERROR: {e}")

    def create_room(self, hotel_id, type_id, room_number, floor_number):
        try:
            room = Room(hotel_id, type_id, room_number, floor_number)
            self.__commit(room)
            return room

        except Exception as e:
            raise DatabaseDriverException(f"Database ERROR: {e}")

    def get_rooms(self, id=None, hotel_id=None, type_id=None, room_number=None, floor_number=None, is_active=None,
                  is_clean=None):
        try:
            rooms = self.__dynamic_filter(Room, locals()).all()
            return rooms

        except Exception as e:
            raise DatabaseDriverException(f"Database ERROR: {e}")

    def update_room(self, id, hotel_id=None, type_id=None, room_number=None, floor_number=None, is_active=None,
                    is_clean=None):
        try:
            room = self.session.query(Room).filter_by(id=id).first()
            room = self.__dynamic_update(Room, locals())
            self.session.commit()
            return room

        except Exception as e:
            raise DatabaseDriverException(f"Database ERROR: {e}")

    def delete_room(self, id):
        try:
            self.session.query(Room).filter_by(id=id).delete()
            self.session.commit()

        except Exception as e:
            self.session.rollback()
            raise DatabaseDriverException(f"Database ERROR: {e}")

    def create_room_type(self, sea_view, pool_view, description, capacity, price_per_night):
        try:
            room_type = RoomType(sea_view, pool_view, description, capacity, price_per_night)
            self.__commit(room_type)
            return room_type

        except Exception as e:
            raise DatabaseDriverException(f"Database ERROR: {e}")

    def get_room_types(self, id=None, sea_view=None, pool_view=None, capacity=None, price_per_night=None):
        try:
            room_types = self.__dynamic_filter(RoomType, locals()).all()
            return room_types

        except Exception as e:
            raise DatabaseDriverException(f"Database ERROR: {e}")

    def update_room_type(self, id, sea_view=None, pool_view=None, capacity=None, price_per_night=None):
        try:
            room_types = self.session.query(RoomType).filter_by(id=id).first()
            room_types = self.__dynamic_update(RoomType, locals())
            self.session.commit()
            return room_types

        except Exception as e:
            raise DatabaseDriverException(f"Database ERROR: {e}")

    def delete_room_type(self, id):
        try:
            self.session.query(RoomType).filter_by(id=id).delete()
            self.session.commit()

        except Exception as e:
            self.session.rollback()
            raise DatabaseDriverException(f"Database ERROR: {e}")

    def create_reservation(self, room_id, guest_id, employee_id, status_id, start_date, end_date, balance):
        try:
            reservation = Reservation(room_id, guest_id, employee_id, status_id, start_date, end_date, balance)
            self.__commit(reservation)
            return reservation

        except Exception as e:
            raise DatabaseDriverException(f"Database ERROR: {e}")

    def get_reservations(self, id=None, room_id=None, guest_id=None, employee_id=None, status_id=None, start_date=None,
                         end_date=None, balance=None):
        try:
            reservations = self.__dynamic_filter(Reservation, locals()).all()
            return reservations

        except Exception as e:
            raise DatabaseDriverException(f"Database ERROR: {e}")

    def update_reservation(self, id, room_id=None, guest_id=None, employee_id=None, status_id=None, start_date=None,
                           end_date=None, balance=None):
        try:
            reservation = self.session.query(Reservation).filter_by(id=id).first()
            reservation = self.__dynamic_update(Room, locals())
            self.session.commit()
            return reservation

        except Exception as e:
            raise DatabaseDriverException(f"Database ERROR: {e}")

    def delete_reservation(self, id):
        try:
            self.session.query(Reservation).filter_by(id=id).delete()
            self.session.commit()

        except Exception as e:
            self.session.rollback()
            raise DatabaseDriverException(f"Database ERROR: {e}")

    def create_reservation_state(self, state: ReservationStatus):
        try:
            reservation_state = ReservationState(state.value)
            self.__commit(reservation_state)
            return reservation_state

        except Exception as e:
            raise DatabaseDriverException(f"Database ERROR: {e}")

    def get_reservation_states(self, id=None, state=None):
        try:
            reservation_states = self.__dynamic_filter(ReservationState, locals()).all()
            return reservation_states

        except Exception as e:
            raise DatabaseDriverException(f"Database ERROR: {e}")

    def delete_reservation_state(self, id):
        try:
            self.session.query(ReservationState).filter_by(id=id).delete()
            self.session.commit()

        except Exception as e:
            self.session.rollback()
            raise DatabaseDriverException(f"Database ERROR: {e}")


if __name__=="__main__":
    db_driver = DBDriver()
