from src.common.miscs import CustomEnum


class HotelClass(CustomEnum):
    CLASS_A = "class_a"
    CLASS_B = "class_b"
    CLASS_C = "class_c"


class ReservationStatus(CustomEnum):
    ON_HOLD = "on_hold"
    CONFIRMED = "confirmed"
    OCCUPIED = "occupied"
    CANCELED = "canceled"
    RELEASED = "released"


class EmployeeRole(CustomEnum):
    ADMIN = "admin"
    MANAGER = "manager"
    RECEPTIONIST = "receptionist"
    HOUSEKEEPING = "housekeeping"


class RolePermissions(CustomEnum):
    CAN_CREATE_HOTEL = "can_create_hotel"
    CAN_GET_HOTEL = "can_get_hotel"
    CAN_UPDATE_HOTEL = "can_update_hotel"
    CAN_DELETE_HOTEL = "can_delete_hotel"
    CAN_CREATE_ROOM = "can_create_room"
    CAN_GET_ROOM = "can_get_room"
    CAN_UPDATE_ROOM = "can_update_room"
    CAN_DELETE_ROOM = "can_delete_room"
    CAN_CREATE_ROOM_TYPE = "can_create_room_type"
    CAN_GET_ROOM_TYPE = "can_get_room_type"
    CAN_UPDATE_ROOM_TYPE = "can_update_room_type"
    CAN_DELETE_ROOM_TYPE = "can_delete_room_type"
    CAN_CREATE_EMPLOYEE = "can_create_employee"
    CAN_GET_EMPLOYEE = "can_get_employee"
    CAN_UPDATE_EMPLOYEE = "can_update_employee"
    CAN_DELETE_EMPLOYEE = "can_delete_employee"
    CAN_CREATE_EMPLOYEE_TYPE = "can_create_employee_type"
    CAN_GET_EMPLOYEE_TYPE = "can_get_employee_type"
    CAN_UPDATE_EMPLOYEE_TYPE = "can_update_employee_type"
    CAN_DELETE_EMPLOYEE_TYPE = "can_delete_employee_type"
    CAN_CREATE_RESERVATION = "can_create_reservation"
    CAN_GET_RESERVATION = "can_get_reservation"
    CAN_UPDATE_RESERVATION = "can_update_reservation"
    CAN_DELETE_RESERVATION = "can_delete_reservation"

