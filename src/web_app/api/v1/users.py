from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from src.db_manager.db_driver import DBDriver
from src.web_app.utils import validate_permission
from src.web_app.standard_response import StandardResponse
from src.db_manager.utils import RolePermissions
from src.common.logger import LogHandler


logger = LogHandler().logger
user_blueprint = Blueprint('user_blueprint', __name__)


@user_blueprint.route('/users/guests', methods=['GET'])
@jwt_required()
@validate_permission(RolePermissions.CAN_GET_GUEST)
def get_guests():
    guests = DBDriver().get_guests()
    return StandardResponse(guests, 200).to_json()


@user_blueprint.route('/users/guests/<guest_id>', methods=['GET'])
@jwt_required()
@validate_permission(RolePermissions.CAN_GET_GUEST)
def get_guest_by_id(guest_id):
    guest = (DBDriver().get_guests(id=guest_id) or [None])[0]

    if not guest:
        return StandardResponse({"error": 'guest not found'}, 404).to_json()

    return StandardResponse(guest, 200).to_json()


@user_blueprint.route('/users/guests/<guest_id>', methods=['PATCH'])
@jwt_required()
@validate_permission(RolePermissions.CAN_UPDATE_GUEST)
def update_guest_by_id(guest_id):
    name = request.json.get("name", None)
    username = request.json.get("username", None)
    email = request.json.get("email", None)

    guest = (DBDriver().get_guests(id=guest_id) or [None])[0]

    if not guest:
        return StandardResponse({"error": 'guest not found'}, 404).to_json()

    try:
        guest = DBDriver().update_guest(guest_id, name, username, email)
        return StandardResponse(guest, 200).to_json()
    except Exception as e:
        logger.error(e)
        return StandardResponse({"error": 'internal server error'}, 500).to_json()


@user_blueprint.route('/users/guests/<guest_id>', methods=['DELETE'])
@jwt_required()
@validate_permission(RolePermissions.CAN_DELETE_GUEST)
def delete_guest(guest_id):
    guest = (DBDriver().get_guests(id=guest_id) or [None])[0]

    if not guest:
        return StandardResponse({"error": 'guest not found'}, 404).to_json()

    try:
        DBDriver().delete_guest(guest_id)
        return StandardResponse({}, 204).to_json()
    except Exception as e:
        logger.error(e)
        return StandardResponse({"error": 'internal server error'}, 400).to_json()


@user_blueprint.route('/users/employees', methods=['GET'])
@jwt_required()
@validate_permission(RolePermissions.CAN_GET_EMPLOYEE)
def get_employees():
    employees = DBDriver().get_employees()
    return StandardResponse(employees, 200).to_json()


@user_blueprint.route('/users/employees/<employee_id>', methods=['GET'])
@jwt_required()
@validate_permission(RolePermissions.CAN_GET_EMPLOYEE)
def get_employee_by_id(employee_id):
    employee = (DBDriver().get_employees(id=employee_id) or [None])[0]

    if employee is None:
        return StandardResponse({"error": 'employee not found'}, 404).to_json()

    return StandardResponse(employee, 200).to_json()


@user_blueprint.route('/users/employees/<employee_id>', methods=['PATCH'])
@jwt_required()
@validate_permission(RolePermissions.CAN_UPDATE_EMPLOYEE)
def update_employee_by_id(employee_id):
    name = request.json.get("name", None)
    username = request.json.get("username", None)
    email = request.json.get("email", None)

    employee = (DBDriver().get_employees(username=username) or [None])[0]

    if not employee:
        return StandardResponse({"error": 'employee not found'}, 404).to_json()

    try:
        employee = DBDriver().update_employee(employee_id, name, username, email)
        return StandardResponse(employee, 200).to_json()
    except Exception as e:
        logger.error(e)
        return StandardResponse({"error": 'internal server error'}, 500).to_json()


@user_blueprint.route('/users/employees/<employee_id>', methods=['DELETE'])
@jwt_required()
@validate_permission(RolePermissions.CAN_DELETE_EMPLOYEE)
def delete_employee(employee_id):
    employee = (DBDriver().get_employees(id=employee_id) or [None])[0]

    if not employee:
        return StandardResponse({"error": 'employee not found'}, 404).to_json()

    try:
        DBDriver().delete_employee(employee_id)
        return StandardResponse({}, 204).to_json()
    except Exception as e:
        logger.error(e)
        return StandardResponse({"error": 'internal server error'}, 400).to_json()



