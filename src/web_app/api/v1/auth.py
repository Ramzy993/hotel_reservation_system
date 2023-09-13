from datetime import timedelta
from flask import Blueprint, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

from src.common.config_manager import ConfigManager
from src.common.logger import LogHandler
from src.db_manager.db_driver import DBDriver
from src.web_app.standard_response import StandardResponse


ACCESS_TOKEN_EXPIRATION_HOURS = ConfigManager().get_int('JWT', 'jwt_access_token_expiration_hours')
auth_blueprint = Blueprint('auth_blueprint', __name__)
logger = LogHandler().logger


@auth_blueprint.route('/guest/register', methods=['POST'])
def register():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    name = request.json.get("name", None)
    email = request.json.get("email", None)

    if None in [username, password, name, email]:
        return StandardResponse({"error": 'username, password, name, email must be in json data'}, 400).to_json()

    try:
        guest = (DBDriver().get_guests(username=username) or [None])[0]

        if guest is not None:
            return StandardResponse({"error": 'guest already found'}, 400).to_json()

        guest = DBDriver().create_guest(username=username, password=password, name=name, email=email)

        return StandardResponse(guest, 200).to_json()
    except Exception as e:
        logger.error(e)
        return StandardResponse({"error": "internal server error"}, 500).to_json()


@auth_blueprint.route('/guest/login', methods=['POST'])
def guest_login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    if username is None or password is None:
        return StandardResponse({"error": 'please provide username and password'}, 400).to_json()

    try:
        guest = (DBDriver().get_guests(username=username) or [None])[0]

        if guest is None:
            return StandardResponse({"error": 'this guest is not registered'}, 404).to_json()

        if not guest.check_password(password):
            return StandardResponse({"error": 'wrong password'}, 401).to_json()

        access_token = create_access_token(identity=username,
                                           expires_delta=timedelta(hours=ACCESS_TOKEN_EXPIRATION_HOURS))

        guest = DBDriver().update_guest_token(id=guest.id, user_token=access_token)

        return StandardResponse({"access_token": access_token, "expiration_date": guest.token_expiration},
                                200).to_json()
    except Exception as e:
        logger.error(e)
        return StandardResponse({"error": "internal server error"}, 500).to_json()


@auth_blueprint.route('/guest/logout', methods=['POST'])
@jwt_required()
def guest_logout():
    current_username = get_jwt_identity()
    guest = DBDriver().get_guests(username=current_username)[0]
    try:
        DBDriver().delete_guest_token(guest.id)
        return StandardResponse({}, 200).to_json()
    except Exception as e:
        logger.error(e)
        return StandardResponse({"error": "internal server error"}, 500).to_json()


@auth_blueprint.route('/employee/login', methods=['POST'])
def employee_login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    if username is None or password is None:
        return StandardResponse({"error": 'please provide username and password'}, 400).to_json()

    try:
        employee = (DBDriver().get_employees(username=username) or [None])[0]

        if employee is None:
            return StandardResponse({"error": 'this guest is not registered'}, 404).to_json()

        if not employee.check_password(password):
            return StandardResponse({"error": 'wrong password'}, 401).to_json()

        access_token = create_access_token(identity=username,
                                           expires_delta=timedelta(hours=ACCESS_TOKEN_EXPIRATION_HOURS))

        employee = DBDriver().update_guest_token(id=employee.id, user_token=access_token)

        return StandardResponse({"access_token": access_token, "expiration_date": employee.token_expiration},
                                200).to_json()
    except Exception as e:
        logger.error(e)
        return StandardResponse({"error": "internal server error"}, 500).to_json()


@auth_blueprint.route('/employee/logout', methods=['POST'])
@jwt_required()
def employee_logout():
    current_username = get_jwt_identity()
    guest = DBDriver().get_employees(username=current_username)[0]
    try:
        DBDriver().delete_employee_token(guest.id)
        return StandardResponse({}, 200).to_json()
    except Exception as e:
        logger.error(e)
        return StandardResponse({"error": "internal server error"}, 500).to_json()
