
from flask import Blueprint, request
from flask_jwt_extended import create_access_token


from src.db_manager.db_driver import DBDriver
from src.web_app.standard_response import StandardResponse


auth_blueprint = Blueprint('auth_blueprint', __name__)


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

        access_token = create_access_token(identity=username)

        DBDriver().update_guest_token(id=guest.id, user_token=access_token)

        return StandardResponse({"access_token": access_token}, 200).to_json()
    except:
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

        access_token = create_access_token(identity=username)

        DBDriver().update_guest_token(id=employee.id, user_token=access_token)

        return StandardResponse({"access_token": access_token}, 200).to_json()
    except:
        return StandardResponse({"error": "internal server error"}, 500).to_json()


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
            return StandardResponse({"error": 'this username is already registered'}, 400).to_json()

        guest = DBDriver().create_guest(username=username, password=password, name=name, email=email)

        return StandardResponse(guest, 200).to_json()
    except:
        return StandardResponse({"error": "internal server error"}, 500).to_json()
