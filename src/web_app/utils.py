from functools import wraps

from flask import request
from flask_jwt_extended import get_jwt_identity

from src.common.logger import LogHandler
from src.db_manager.db_driver import DBDriver
from src.web_app.standard_response import StandardResponse
from src.db_manager.utils import RolePermissions

logger = LogHandler().logger


def validate_permission(permission: RolePermissions):
    def decorator(function):
        @wraps(function)
        def decorated_function(*args, **kwargs):
            current_username = get_jwt_identity()

            # TODO: better user request.current_user in request lifetime
            request.current_user = (DBDriver().get_guests(username=current_username) +
                                    DBDriver().get_employees(username=current_username))[0]

            if permission.value in request.current_user.user_type.permissions:
                return function(*args, **kwargs)

            return StandardResponse({"error": 'not authorized'}, 401).to_json()
        return decorated_function
    return decorator
