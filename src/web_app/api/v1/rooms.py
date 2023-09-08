from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity, jwt_required


from src.db_manager.db_driver import DBDriver
from src.web_app.utils import validate_permission
from src.web_app.standard_response import StandardResponse
from src.db_manager.utils import RolePermissions


room_blueprint = Blueprint('room_blueprint', __name__)


@room_blueprint.route('/rooms', methods=['GET'])
@jwt_required()
@validate_permission(RolePermissions.CAN_GET_ROOM.value)
def get_rooms():
    rooms = DBDriver().get_rooms()
    return StandardResponse(rooms, 200).to_json()


@room_blueprint.route('/rooms/<room_id>', methods=['GET'])
@jwt_required()
@validate_permission(RolePermissions.CAN_GET_ROOM.value)
def get_room(room_id):
    room = DBDriver().get_rooms(id=room_id)[0]
    return StandardResponse(room, 200).to_json()


@room_blueprint.route('/rooms', methods=['POST'])
@jwt_required()
@validate_permission(RolePermissions.CAN_CREATE_ROOM.value)
def create_room():
    hotel_id = request.json.get("hotel_id", None)
    type_id = request.json.get("type_id", None)
    room_number = request.json.get("room_number", None)
    floor_number = request.json.get("floor_number", None)
    try:
        room = DBDriver().create_room(hotel_id, type_id, room_number, floor_number)
        return StandardResponse(room, 201).to_json()
    except:
        return StandardResponse({"error": 'some values are missing'}, 400).to_json()


@room_blueprint.route('/rooms/<room_id>', methods=['PUT', 'PATCH'])
@jwt_required()
@validate_permission(RolePermissions.CAN_UPDATE_ROOM.value)
def update_room(room_id):
    hotel_id = request.json.get("hotel_id", None)
    type_id = request.json.get("type_id", None)
    room_number = request.json.get("room_number", None)
    floor_number = request.json.get("floor_number", None)
    is_active = request.json.get("is_active", None)
    is_clean = request.json.get("is_clean", None)
    try:
        room = DBDriver().update_room(room_id, hotel_id, type_id, room_number, floor_number, is_active, is_clean)
        return StandardResponse(room, 200).to_json()
    except:
        return StandardResponse({"error": 'some values are missing'}, 400).to_json()


@room_blueprint.route('/rooms/<room_id>', methods=['DELETE'])
@jwt_required()
@validate_permission(RolePermissions.CAN_DELETE_ROOM.value)
def delete_room(room_id):
    try:
        DBDriver().delete_room(room_id)
        return StandardResponse({}, 204).to_json()
    except:
        return StandardResponse({"error": 'some values are missing'}, 400).to_json()



