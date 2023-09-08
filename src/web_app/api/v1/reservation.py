from flask import Blueprint, request
from flask_jwt_extended import jwt_required


from src.db_manager.db_driver import DBDriver
from src.web_app.utils import validate_permission
from src.web_app.standard_response import StandardResponse
from src.db_manager.utils import RolePermissions, ReservationStatus


reservation_blueprint = Blueprint('reservation_blueprint', __name__)


@reservation_blueprint.route('/reservations', methods=['GET'])
@jwt_required()
@validate_permission(RolePermissions.CAN_GET_RESERVATION.value)
def get_reservations():
    reservations = DBDriver().get_reservations()
    return StandardResponse(reservations, 200).to_json()


@reservation_blueprint.route('/reservations/<reservation_id>', methods=['GET'])
@jwt_required()
@validate_permission(RolePermissions.CAN_GET_RESERVATION.value)
def get_reservation(reservation_id):
    reservation = DBDriver().get_reservations(id=reservation_id)[0]
    return StandardResponse(reservation, 200).to_json()


@reservation_blueprint.route('/reservations/on_hold', methods=['POST'])
@jwt_required()
@validate_permission(RolePermissions.CAN_CREATE_RESERVATION.value)
def create_room():
    room_id = request.json.get("room_id", None)
    guest_id = request.json.get("guest_id", None)
    employee_id = request.json.get("employee_id", None)
    start_date = request.json.get("start_date", None)
    end_date = request.json.get("end_date", None)

    reservation_in_this_time = DBDriver().get_reservation_for_room_in_period(room_id=room_id, from_date=start_date,
                                                                             to_date=end_date)

    if len(reservation_in_this_time) > 0:
        return StandardResponse({"error": 'reservation not available'}, 404).to_json()

    on_hold_id = DBDriver().get_reservation_states(state=ReservationStatus.ON_HOLD.value)[0].id
    try:
        price_per_night = DBDriver().get_rooms(id=room_id)[0].type_.price_per_night
        balance = (end_date - start_date).days * price_per_night
        reservation = DBDriver().create_reservation(room_id=room_id, guest_id=guest_id, employee_id=employee_id,
                                                    status_id=on_hold_id, start_date=start_date, end_date=end_date,
                                                    balance=balance)
        return StandardResponse(reservation, 201).to_json()
    except:
        return StandardResponse({"error": 'some values are missing'}, 400).to_json()


@reservation_blueprint.route('/reservations/<reservation_id>/confirmed', methods=['PATCH'])
@jwt_required()
@validate_permission(RolePermissions.CAN_UPDATE_RESERVATION.value)
def update_reservation_to_confirmed(reservation_id):

    try:
        confirmed_id = DBDriver().get_reservation_states(state=ReservationStatus.CONFIRMED.value)[0].id
        reservation = DBDriver().update_reservation(id=reservation_id, status_id=confirmed_id)
        return StandardResponse(reservation, 200).to_json()
    except:
        return StandardResponse({"error": 'some values are missing'}, 400).to_json()


@reservation_blueprint.route('/reservations/<reservation_id>/occupied', methods=['PATCH'])
@jwt_required()
@validate_permission(RolePermissions.CAN_UPDATE_RESERVATION.value)
def update_reservation_to_occupied(reservation_id):

    try:
        occupied_id = DBDriver().get_reservation_states(state=ReservationStatus.OCCUPIED.value)[0].id
        reservation = DBDriver().update_reservation(id=reservation_id, status_id=occupied_id)
        return StandardResponse(reservation, 200).to_json()
    except:
        return StandardResponse({"error": 'some values are missing'}, 400).to_json()


@reservation_blueprint.route('/reservations/<reservation_id>/canceled', methods=['PATCH'])
@jwt_required()
@validate_permission(RolePermissions.CAN_UPDATE_RESERVATION.value)
def update_reservation_to_canceled(reservation_id):

    try:
        canceled_id = DBDriver().get_reservation_states(state=ReservationStatus.CANCELED.value)[0].id
        reservation = DBDriver().update_reservation(id=reservation_id, status_id=canceled_id)
        return StandardResponse(reservation, 200).to_json()
    except:
        return StandardResponse({"error": 'some values are missing'}, 400).to_json()


@reservation_blueprint.route('/reservations/<reservation_id>/released', methods=['PATCH'])
@jwt_required()
@validate_permission(RolePermissions.CAN_UPDATE_RESERVATION.value)
def update_reservation_to_released(reservation_id):

    try:
        released_id = DBDriver().get_reservation_states(state=ReservationStatus.RELEASED.value)[0].id
        reservation = DBDriver().update_reservation(id=reservation_id, status_id=released_id)
        return StandardResponse(reservation, 200).to_json()
    except:
        return StandardResponse({"error": 'some values are missing'}, 400).to_json()


@reservation_blueprint.route('/reservations/<reservation_id>', methods=['PATCH'])
@jwt_required()
@validate_permission(RolePermissions.CAN_UPDATE_RESERVATION.value)
def update_reservation(reservation_id):

    try:
        released_id = DBDriver().get_reservation_states(state=ReservationStatus.RELEASED.value)[0].id
        reservation = DBDriver().update_reservation(id=reservation_id, status_id=released_id)
        return StandardResponse(reservation, 200).to_json()
    except:
        return StandardResponse({"error": 'some values are missing'}, 400).to_json()
